/**
 * SOVEREIGN PWA — Backend Wiring Code
 *
 * This file contains all the JavaScript functions needed to wire
 * the SOVEREIGN dashboard to real data. Copy these into your PWA's
 * main JavaScript file or import as a module.
 *
 * Dependencies: None (uses fetch API)
 * Connects to: Supabase, Claude API, Google Calendar
 */

// ============================================================
// CONFIG
// ============================================================
const SUPABASE_URL = 'https://pjkurxtvvtxbpfearqhd.supabase.co';
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY || '';     // Set in .env or Vercel env vars
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY || ''; // Server-side ONLY — never expose client-side
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY || '';       // Set in .env or Vercel env vars

const SUPABASE_HEADERS = {
  'apikey': SUPABASE_ANON_KEY,
  'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
  'Content-Type': 'application/json'
};

const SUPABASE_SERVICE_HEADERS = {
  'apikey': SUPABASE_SERVICE_KEY,
  'Authorization': `Bearer ${SUPABASE_SERVICE_KEY}`,
  'Content-Type': 'application/json'
};

// ============================================================
// 1. COMMS TAB — CEO CHAT via Claude API
// ============================================================

/**
 * Load a CEO's brain (system prompt) from Supabase
 */
async function loadCEOBrain(ceoId) {
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/ceo_brains?id=eq.${ceoId}&select=system_prompt`,
    { headers: SUPABASE_HEADERS }
  );
  const data = await res.json();
  return data[0]?.system_prompt || '';
}

/**
 * Load a CEO's memories from Supabase
 */
async function loadCEOMemories(ceoId) {
  // Get CEO's own memories
  const own = await fetch(
    `${SUPABASE_URL}/rest/v1/ceo_memories?ceo_id=eq.${ceoId}&select=title,content,category,importance&order=importance.desc&limit=20`,
    { headers: SUPABASE_HEADERS }
  );
  const ownData = await own.json();

  // Get shared memories relevant to this CEO
  const shared = await fetch(
    `${SUPABASE_URL}/rest/v1/ceo_memories?memory_type=eq.shared&select=title,content,category,importance&order=importance.desc&limit=10`,
    { headers: SUPABASE_HEADERS }
  );
  const sharedData = await shared.json();

  return { own: ownData, shared: sharedData };
}

/**
 * Load tech stack from system_config
 */
async function loadTechStack() {
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/system_config?key=in.(tech_stack,skills_and_repos)`,
    { headers: SUPABASE_HEADERS }
  );
  return await res.json();
}

/**
 * Build the full context for a CEO conversation
 */
async function buildCEOContext(ceoId) {
  const [brain, memories, techStack] = await Promise.all([
    loadCEOBrain(ceoId),
    loadCEOMemories(ceoId),
    loadTechStack()
  ]);

  const memoryText = memories.own
    .map(m => `[${m.category}] ${m.title}: ${m.content}`)
    .join('\n\n');

  const sharedText = memories.shared
    .map(m => `[SHARED] ${m.title}: ${m.content}`)
    .join('\n\n');

  const techText = techStack
    .map(t => `${t.key}: ${JSON.stringify(t.value).substring(0, 500)}`)
    .join('\n\n');

  const systemPrompt = `${brain}

--- MEMORIES (Query from ceo_memories) ---
${memoryText}

--- SHARED INTEL ---
${sharedText}

--- TECH STACK (Query from system_config) ---
${techText}`;

  return systemPrompt;
}

/**
 * Send a message to a CEO via Claude API
 * Returns the CEO's response
 */
async function chatWithCEO(ceoId, userMessage, conversationHistory = []) {
  const systemPrompt = await buildCEOContext(ceoId);

  const messages = [
    ...conversationHistory,
    { role: 'user', content: userMessage }
  ];

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: 4096,
      system: systemPrompt,
      messages: messages
    })
  });

  const data = await res.json();
  const reply = data.content?.[0]?.text || 'Error: No response';

  // Store in ceo_messages
  await fetch(`${SUPABASE_URL}/rest/v1/ceo_messages`, {
    method: 'POST',
    headers: SUPABASE_SERVICE_HEADERS,
    body: JSON.stringify({
      ceo_id: ceoId,
      role: 'user',
      content: userMessage
    })
  });

  await fetch(`${SUPABASE_URL}/rest/v1/ceo_messages`, {
    method: 'POST',
    headers: SUPABASE_SERVICE_HEADERS,
    body: JSON.stringify({
      ceo_id: ceoId,
      role: 'assistant',
      content: reply
    })
  });

  return reply;
}

/**
 * Load chat history for a CEO
 */
async function loadChatHistory(ceoId, limit = 50) {
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/ceo_messages?ceo_id=eq.${ceoId}&select=role,content,created_at&order=created_at.desc&limit=${limit}`,
    { headers: SUPABASE_HEADERS }
  );
  const data = await res.json();
  return data.reverse(); // Chronological order
}


// ============================================================
// 2. HOME TAB — Real Supabase Data
// ============================================================

/**
 * Load dashboard stats
 */
async function loadDashboardStats() {
  const [aegisStats, ceoMemoryCounts, lifeGoals, revenue] = await Promise.all([
    fetch(`${SUPABASE_URL}/rest/v1/aegis_dashboard_stats`, { headers: SUPABASE_HEADERS }).then(r => r.json()),
    fetch(`${SUPABASE_URL}/rest/v1/ceo_memories?select=ceo_id`, { headers: SUPABASE_HEADERS }).then(r => r.json()),
    fetch(`${SUPABASE_URL}/rest/v1/life_goals`, { headers: SUPABASE_HEADERS }).then(r => r.json()),
    fetch(`${SUPABASE_URL}/rest/v1/aegis_revenue?select=amount,paid`, { headers: SUPABASE_HEADERS }).then(r => r.json())
  ]);

  // Count memories per CEO
  const memoryCounts = {};
  ceoMemoryCounts.forEach(m => {
    memoryCounts[m.ceo_id] = (memoryCounts[m.ceo_id] || 0) + 1;
  });

  // Calculate real revenue
  const totalRevenue = revenue
    .filter(r => r.paid)
    .reduce((sum, r) => sum + parseFloat(r.amount || 0), 0);

  return {
    aegis: aegisStats[0] || {},
    memoryCounts,
    lifeGoals,
    totalRevenue,
    mrr: 0 // Will update when real revenue flows
  };
}

/**
 * Load CEO status cards with real data
 */
async function loadCEOStatuses() {
  const ceos = ['zero', 'apex', 'midas', 'aegis'];
  const statuses = {};

  for (const ceo of ceos) {
    const [brain, memories, messages] = await Promise.all([
      fetch(`${SUPABASE_URL}/rest/v1/ceo_brains?id=eq.${ceo}&select=name,business`, { headers: SUPABASE_HEADERS }).then(r => r.json()),
      fetch(`${SUPABASE_URL}/rest/v1/ceo_memories?ceo_id=eq.${ceo}&select=id`, { headers: SUPABASE_HEADERS }).then(r => r.json()),
      fetch(`${SUPABASE_URL}/rest/v1/ceo_messages?ceo_id=eq.${ceo}&select=id&order=created_at.desc&limit=5`, { headers: SUPABASE_HEADERS }).then(r => r.json())
    ]);

    statuses[ceo] = {
      name: brain[0]?.name || ceo.toUpperCase(),
      business: brain[0]?.business || '',
      memories: memories.length,
      unread: messages.length,
      status: 'active'
    };
  }

  return statuses;
}

/**
 * Load calendar events
 */
async function loadCalendarEvents() {
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/system_config?key=eq.calendar_events`,
    { headers: SUPABASE_HEADERS }
  );
  const data = await res.json();
  return data[0]?.value?.events || [];
}


// ============================================================
// 3. LIFE TAB — XP System with Real Tracking
// ============================================================

/**
 * Load XP data
 */
async function loadXP() {
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/system_config?key=eq.life_xp`,
    { headers: SUPABASE_HEADERS }
  );
  const data = await res.json();
  return data[0]?.value || null;
}

/**
 * Award XP for an action
 */
async function awardXP(action) {
  const xpData = await loadXP();
  if (!xpData) return;

  const points = xpData.xp_actions[action] || 0;
  if (points === 0) return;

  xpData.total_xp += points;
  xpData.xp_in_level += points;

  // Check level up
  const levels = Object.entries(xpData.levels).sort((a, b) => b[1].xp - a[1].xp);
  for (const [lvl, info] of levels) {
    if (xpData.total_xp >= info.xp) {
      xpData.level = parseInt(lvl);
      xpData.level_name = info.name;
      const nextLevel = xpData.levels[String(parseInt(lvl) + 1)];
      if (nextLevel) {
        xpData.xp_to_next = nextLevel.xp - xpData.total_xp;
        xpData.xp_in_level = xpData.total_xp - info.xp;
      }
      break;
    }
  }

  // Update streak
  const today = new Date().toISOString().split('T')[0];
  if (xpData.last_active_date !== today) {
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    if (xpData.last_active_date === yesterday) {
      xpData.streak_days += 1;
    } else if (xpData.last_active_date !== today) {
      xpData.streak_days = 1;
    }
    xpData.last_active_date = today;
    xpData.streak_best = Math.max(xpData.streak_best, xpData.streak_days);

    // Update weekly hits
    const dayOfWeek = new Date().getDay();
    const mondayIndex = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    xpData.weekly_hits[mondayIndex] = true;
  }

  // Check achievements
  if (action === 'deal_closed') {
    const firstSale = xpData.achievements.find(a => a.id === 'first_sale');
    if (firstSale && !firstSale.earned) {
      firstSale.earned = true;
      xpData.total_xp += 50; // Bonus XP for achievement
    }
  }
  if (xpData.streak_days >= 3) {
    const streak3 = xpData.achievements.find(a => a.id === 'streak_3');
    if (streak3) streak3.earned = true;
  }
  if (xpData.streak_days >= 7) {
    const streak7 = xpData.achievements.find(a => a.id === 'streak_7');
    if (streak7) streak7.earned = true;
  }

  // Save back to Supabase
  await fetch(`${SUPABASE_URL}/rest/v1/system_config?key=eq.life_xp`, {
    method: 'PATCH',
    headers: SUPABASE_SERVICE_HEADERS,
    body: JSON.stringify({ value: xpData })
  });

  return { points, total: xpData.total_xp, level: xpData.level, levelName: xpData.level_name };
}

/**
 * Complete a daily challenge
 */
async function completeDailyChallenge(challengeId) {
  const xpData = await loadXP();
  const challenge = xpData.daily_challenges.find(c => c.id === challengeId);
  if (!challenge || challenge.completed) return null;

  challenge.completed = true;
  const result = await awardXP('task_complete');

  await fetch(`${SUPABASE_URL}/rest/v1/system_config?key=eq.life_xp`, {
    method: 'PATCH',
    headers: SUPABASE_SERVICE_HEADERS,
    body: JSON.stringify({ value: xpData })
  });

  return result;
}

/**
 * Log a workout
 */
async function logWorkout(type) {
  return await awardXP('workout_logged');
}


// ============================================================
// 4. MONEY TAB — Real Financial Data
// ============================================================

/**
 * Load revenue by business
 */
async function loadRevenue() {
  const [aegisRevenue, aegisAdSpend] = await Promise.all([
    fetch(`${SUPABASE_URL}/rest/v1/aegis_revenue?select=amount,type,paid,created_at&order=created_at.desc`, { headers: SUPABASE_HEADERS }).then(r => r.json()),
    fetch(`${SUPABASE_URL}/rest/v1/aegis_ad_spend?select=amount,platform,leads_generated,date&order=date.desc`, { headers: SUPABASE_HEADERS }).then(r => r.json())
  ]);

  const totalPaid = aegisRevenue.filter(r => r.paid).reduce((s, r) => s + parseFloat(r.amount), 0);
  const totalSpend = aegisAdSpend.reduce((s, r) => s + parseFloat(r.amount), 0);

  return {
    aegis: { revenue: totalPaid, adSpend: totalSpend, profit: totalPaid - totalSpend },
    zero: { revenue: 0, note: 'Awaiting first client payment' },
    midas: { revenue: 0, note: 'Awaiting LLC formation + first outreach' },
    apex: { revenue: 0, note: 'Awaiting storefront launch' },
    total: totalPaid,
    totalExpenses: totalSpend,
    netProfit: totalPaid - totalSpend
  };
}


// ============================================================
// 5. REALTIME — Supabase Subscriptions
// ============================================================

/**
 * Subscribe to real-time changes on aegis_leads
 * Requires Supabase JS client (import from CDN or npm)
 */
function subscribeToLeads(callback) {
  // Add this to your HTML: <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  // const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  // const channel = supabase.channel('aegis-leads')
  //   .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'aegis_leads' }, payload => {
  //     callback(payload.new);
  //   })
  //   .subscribe();
  // return channel;
  console.log('Realtime subscriptions require Supabase JS client');
}


// ============================================================
// EXPORTS (for module usage)
// ============================================================
if (typeof module !== 'undefined') {
  module.exports = {
    chatWithCEO, loadChatHistory, buildCEOContext,
    loadDashboardStats, loadCEOStatuses, loadCalendarEvents,
    loadXP, awardXP, completeDailyChallenge, logWorkout,
    loadRevenue, subscribeToLeads
  };
}
