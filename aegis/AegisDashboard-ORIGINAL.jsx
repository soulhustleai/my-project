import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Phone, TrendingUp, Users, Clock, DollarSign, Zap, ChevronRight, CheckCircle2, AlertCircle, ArrowUpRight, ArrowDownRight, Star, PhoneCall, PhoneOff, PhoneMissed, Timer, Target, BarChart3, PieChart, Activity, X, FileText, Award, Flame, ChevronUp, Bell } from 'lucide-react';
import { fetchAegisDashboardStats } from '../lib/supabase';

// ─── AEGIS Navy Blue theme ───
const AEGIS = {
  navy: '#1E3A5F',
  navyLight: '#2A4A70',
  gold: '#D4AF37',
  green: '#10B981',
  red: '#EF4444',
  amber: '#F59E0B',
  cyan: '#06B6D4',
  dark: '#050A12',
  bg: '#0D1F35',
};

// ─── CSS Keyframes injected once ───
const CONFETTI_STYLES = `
@keyframes aegis-confetti-fall {
  0% { transform: translateY(-10px) rotate(0deg); opacity: 1; }
  100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}
@keyframes aegis-sparkle {
  0%, 100% { transform: scale(0) rotate(0deg); opacity: 0; }
  50% { transform: scale(1) rotate(180deg); opacity: 1; }
}
@keyframes aegis-pulse-ring {
  0% { transform: scale(0.8); opacity: 0.8; }
  100% { transform: scale(1.6); opacity: 0; }
}
@keyframes aegis-ticker-scroll {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
@keyframes aegis-glow {
  0%, 100% { box-shadow: 0 0 5px rgba(212,175,55,0.3); }
  50% { box-shadow: 0 0 20px rgba(212,175,55,0.6); }
}
`;

// ─── Demo data ───
const DEMO_DATA = {
  today: {
    leadsReceived: 12,
    leadsContacted: 9,
    quotesGiven: 6,
    closed: 3,
    revenue: 1275,
    avgResponseTime: '2m 14s',
    closeRate: 33,
    hotQueue: 3,
    dailyGoal: 5,
  },
  week: {
    leadsReceived: 67,
    closed: 14,
    revenue: 5950,
    closeRate: 21,
    costPerLead: 12.40,
    costPerClose: 59.20,
  },
  month: {
    leadsReceived: 234,
    closed: 52,
    revenue: 22100,
    adSpend: 2800,
    roi: 689,
    projectedAnnual: 265200,
  },
  hotLeads: [
    { id: 1, name: 'Marcus J.', score: 94, tier: 'A', reason: 'Lost job 3 days ago, COBRA expiring', phone: '(718) 555-0142', timeInQueue: 4, source: 'Facebook', type: 'job_loss' },
    { id: 2, name: 'Tanya W.', score: 88, tier: 'A', reason: 'Pregnant, no coverage, due in 5 months', phone: '(347) 555-0198', timeInQueue: 11, source: 'Google', type: 'life_event' },
    { id: 3, name: 'Jerome K.', score: 82, tier: 'A', reason: 'Turning 26, off parents plan next week', phone: '(917) 555-0267', timeInQueue: 23, source: 'Referral', type: 'aging_out' },
  ],
  recentActivity: [
    { time: '2 min ago', action: 'Lead closed', name: 'Robert S.', detail: 'BlueCross Silver Plan — $340/mo', amount: '$100', type: 'close' },
    { time: '18 min ago', action: 'Quote sent', name: 'Lisa M.', detail: 'Aetna Gold + Dental', type: 'quote' },
    { time: '34 min ago', action: 'Lead contacted', name: 'DeShawn T.', detail: 'First call — scheduling follow-up Thu', type: 'contact' },
    { time: '1h ago', action: 'Lead closed', name: 'Patricia G.', detail: 'United Healthcare Bronze — $180/mo', amount: '$75', type: 'close' },
    { time: '1.5h ago', action: 'New lead', name: 'Andre B.', detail: 'Score: 91 — Job loss, needs coverage ASAP', type: 'new' },
  ],
  sourceBreakdown: [
    { name: 'Facebook Ads', leads: 98, closes: 22, rate: 22, cost: 1400, color: AEGIS.cyan },
    { name: 'Google Ads', leads: 62, closes: 16, rate: 26, cost: 900, color: AEGIS.green },
    { name: 'Referrals', leads: 34, closes: 8, rate: 24, cost: 0, color: AEGIS.gold },
    { name: 'Organic/Content', leads: 24, closes: 4, rate: 17, cost: 200, color: AEGIS.amber },
    { name: 'Partnerships', leads: 16, closes: 2, rate: 13, cost: 300, color: AEGIS.navy },
  ],
  weeklyTrend: [
    { day: 'Mon', leads: 11, closes: 2 },
    { day: 'Tue', leads: 14, closes: 3 },
    { day: 'Wed', leads: 9, closes: 2 },
    { day: 'Thu', leads: 12, closes: 4 },
    { day: 'Fri', leads: 8, closes: 1 },
    { day: 'Sat', leads: 7, closes: 1 },
    { day: 'Sun', leads: 6, closes: 1 },
  ],
  streak: { count: 3, agent: 'DayDay' },
  leaderboard: {
    agent: 'DayDay',
    rank: 1,
    closeRate: 33,
    speedToContact: '2m 14s',
    revenue: 1275,
    qualityScore: 92,
  },
};

// ─── Call Script Data ───
const CALL_SCRIPTS = {
  job_loss: {
    label: 'Job Loss / COBRA',
    color: AEGIS.red,
    lines: [
      'I understand losing your job is stressful — let me help take one worry off your plate.',
      'COBRA can cost $600+/mo. I can usually find comparable coverage for half that.',
      'Qualifying life event = immediate enrollment, no waiting period.',
      'Ask: When did you lose coverage? Any prescriptions or doctors to keep?',
    ],
  },
  open_enrollment: {
    label: 'Open Enrollment',
    color: AEGIS.cyan,
    lines: [
      'Open enrollment ends [DATE] — let\'s make sure you\'re covered.',
      'Compare 3+ plans side by side. Most people overpay by $100+/mo.',
      'I\'ll check if you qualify for subsidies — many people leave money on the table.',
      'Ask: What\'s your household size and estimated income?',
    ],
  },
  self_employed: {
    label: 'Self-Employed',
    color: AEGIS.gold,
    lines: [
      'Self-employed? You probably qualify for marketplace subsidies most people miss.',
      'Your premium is tax-deductible — I can show you how to maximize savings.',
      'Plans with HSA compatibility = double tax advantage for entrepreneurs.',
      'Ask: Is this just for you or family too? Any expected medical needs?',
    ],
  },
  life_event: {
    label: 'Life Event (Baby, Marriage)',
    color: AEGIS.green,
    lines: [
      'Congratulations! A new baby/marriage triggers a Special Enrollment Period.',
      'You have 60 days from the event to enroll — let\'s not waste time.',
      'Prenatal and pediatric care are essential health benefits on all ACA plans.',
      'Ask: What\'s the event date? Any specific doctors or hospitals you need?',
    ],
  },
  aging_out: {
    label: 'Turning 26 / Aging Out',
    color: AEGIS.amber,
    lines: [
      'You\'re about to age off your parents\' plan — it happens fast.',
      'Good news: this is a qualifying event, so you can enroll immediately.',
      'Most young adults can find solid coverage for $150-300/mo, sometimes less with subsidies.',
      'Ask: Any medications? Preferred doctors? What\'s your budget look like?',
    ],
  },
};

// ═══════════════════════════════════════════════════════════════
// HOOKS
// ═══════════════════════════════════════════════════════════════

// Animated counter hook using requestAnimationFrame
function useAnimatedCounter(target, duration = 1500, prefix = '', decimals = 0) {
  const [display, setDisplay] = useState(0);
  const startTime = useRef(null);
  const rafId = useRef(null);

  useEffect(() => {
    startTime.current = null;
    const animate = (timestamp) => {
      if (!startTime.current) startTime.current = timestamp;
      const elapsed = timestamp - startTime.current;
      const progress = Math.min(elapsed / duration, 1);
      // easeOutExpo
      const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      setDisplay(eased * target);
      if (progress < 1) {
        rafId.current = requestAnimationFrame(animate);
      }
    };
    rafId.current = requestAnimationFrame(animate);
    return () => { if (rafId.current) cancelAnimationFrame(rafId.current); };
  }, [target, duration]);

  const val = decimals > 0 ? display.toFixed(decimals) : Math.round(display);
  return `${prefix}${Number(val).toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })}`;
}

// Live timer hook (returns elapsed seconds since mount, ticking every second)
function useLiveTimer(initialMinutes) {
  const [elapsed, setElapsed] = useState(initialMinutes * 60);
  useEffect(() => {
    const iv = setInterval(() => setElapsed(e => e + 1), 1000);
    return () => clearInterval(iv);
  }, []);
  return elapsed;
}

// ═══════════════════════════════════════════════════════════════
// SUB-COMPONENTS
// ═══════════════════════════════════════════════════════════════

// 1. Daily Goal Progress Ring (SVG)
function DailyGoalRing({ closed, goal }) {
  const pct = Math.min((closed / goal) * 100, 100);
  const radius = 44;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (pct / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-28 h-28">
        <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
          <defs>
            <linearGradient id="goalGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={AEGIS.gold} />
              <stop offset="100%" stopColor={AEGIS.green} />
            </linearGradient>
          </defs>
          {/* Background ring */}
          <circle cx="50" cy="50" r={radius} fill="none" stroke="#1E3A5F" strokeWidth="6" opacity="0.3" />
          {/* Progress ring */}
          <motion.circle
            cx="50" cy="50" r={radius}
            fill="none"
            stroke="url(#goalGrad)"
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.5, ease: 'easeOut' }}
          />
        </svg>
        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-bold text-white">{closed}/{goal}</span>
          <span className="text-[8px] text-white/40 uppercase tracking-wider">closes</span>
        </div>
      </div>
      <p className="text-[9px] text-[#D4AF37]/60 uppercase tracking-widest mt-1">Daily Goal</p>
    </div>
  );
}

// 2. Lead Score Ring (SVG arc)
function LeadScoreRing({ score, size = 32 }) {
  const maxScore = 100;
  const pct = (score / maxScore) * 100;
  const r = (size / 2) - 3;
  const circumference = 2 * Math.PI * r;
  const offset = circumference - (pct / 100) * circumference;

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg viewBox={`0 0 ${size} ${size}`} className="w-full h-full -rotate-90">
        <defs>
          <linearGradient id={`scoreGrad-${score}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={AEGIS.gold} />
            <stop offset="100%" stopColor={AEGIS.green} />
          </linearGradient>
        </defs>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="#1E3A5F" strokeWidth="2.5" opacity="0.3" />
        <motion.circle
          cx={size/2} cy={size/2} r={r}
          fill="none"
          stroke={`url(#scoreGrad-${score})`}
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-[10px] font-bold text-white">{score}</span>
      </div>
    </div>
  );
}

// 3. Speed-to-Contact Timer
function SpeedTimer({ initialMinutes }) {
  const elapsed = useLiveTimer(initialMinutes);
  const mins = Math.floor(elapsed / 60);
  const secs = elapsed % 60;
  const color = mins < 2 ? AEGIS.green : mins < 5 ? AEGIS.amber : AEGIS.red;
  const label = mins < 2 ? 'FAST' : mins < 5 ? 'HURRY' : 'URGENT';

  return (
    <div className="flex items-center gap-1">
      <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ backgroundColor: color }} />
      <span className="text-[9px] font-mono font-bold" style={{ color }}>
        {mins}:{secs.toString().padStart(2, '0')}
      </span>
      <span className="text-[7px] font-bold px-1 py-0.5 rounded" style={{ backgroundColor: `${color}20`, color }}>{label}</span>
    </div>
  );
}

// 4. Confetti Celebration
function ConfettiCelebration({ active, onDone }) {
  const [pieces, setPieces] = useState([]);

  useEffect(() => {
    if (!active) return;
    const colors = [AEGIS.gold, AEGIS.green, AEGIS.cyan, AEGIS.amber, '#fff'];
    const newPieces = Array.from({ length: 40 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 0.5,
      duration: 1.5 + Math.random() * 1.5,
      color: colors[Math.floor(Math.random() * colors.length)],
      size: 4 + Math.random() * 6,
      type: Math.random() > 0.5 ? 'circle' : 'rect',
    }));
    setPieces(newPieces);
    const timer = setTimeout(() => { setPieces([]); onDone && onDone(); }, 3000);
    return () => clearTimeout(timer);
  }, [active]);

  if (!pieces.length) return null;

  return (
    <div className="fixed inset-0 z-50 pointer-events-none overflow-hidden">
      {pieces.map(p => (
        <div
          key={p.id}
          className={p.type === 'circle' ? 'rounded-full' : 'rounded-sm'}
          style={{
            position: 'absolute',
            left: `${p.left}%`,
            top: '-10px',
            width: p.size,
            height: p.type === 'rect' ? p.size * 1.5 : p.size,
            backgroundColor: p.color,
            animation: `aegis-confetti-fall ${p.duration}s ease-in ${p.delay}s forwards`,
          }}
        />
      ))}
      {/* Central sparkle burst */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2">
        {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 rounded-full"
            style={{
              backgroundColor: AEGIS.gold,
              transform: `rotate(${angle}deg) translateY(-30px)`,
              animation: `aegis-sparkle 0.8s ease-out ${i * 0.05}s forwards`,
            }}
          />
        ))}
      </div>
    </div>
  );
}

// 5. Earnings Ticker
function EarningsTicker({ todayRevenue, monthRevenue }) {
  const items = [
    `TODAY: $${todayRevenue.toLocaleString()} earned`,
    `THIS MONTH: $${monthRevenue.toLocaleString()} revenue`,
    `NET PROFIT: $${(monthRevenue - 2800).toLocaleString()}`,
    `ROI: 689% return on ad spend`,
    `STREAK: 3 consecutive closes`,
  ];

  return (
    <div className="w-full overflow-hidden bg-[#0D1F35]/80 border-b border-[#1E3A5F]/20 py-1">
      <div className="flex whitespace-nowrap" style={{ animation: 'aegis-ticker-scroll 25s linear infinite' }}>
        {[...items, ...items].map((item, i) => (
          <span key={i} className="text-[9px] font-mono mx-6">
            <span className="text-[#D4AF37]/60">|</span>
            <span className="text-[#D4AF37] ml-2">{item}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

// 6. Smart Notification Banner
function SmartNotificationBanner({ leads, closeRate }) {
  const [currentTip, setCurrentTip] = useState(0);

  const urgentLeads = leads.filter(l => l.timeInQueue > 5);
  const tips = [];

  if (urgentLeads.length > 0) {
    const hottest = urgentLeads.sort((a, b) => b.score - a.score)[0];
    tips.push({
      type: 'urgent',
      text: `${urgentLeads.length} lead${urgentLeads.length > 1 ? 's' : ''} waiting 5+ min — call ${hottest.name} first (score: ${hottest.score})`,
      color: AEGIS.red,
    });
  }

  if (closeRate > 25) {
    tips.push({ type: 'positive', text: `Close rate is ${closeRate}% today — above average! Keep the momentum.`, color: AEGIS.green });
  } else {
    tips.push({ type: 'coaching', text: `Close rate is ${closeRate}% — try leading with urgency on the next call.`, color: AEGIS.amber });
  }

  tips.push({ type: 'tip', text: 'Pro tip: Leads contacted within 2 minutes close 3x more often.', color: AEGIS.cyan });

  useEffect(() => {
    if (tips.length <= 1) return;
    const iv = setInterval(() => setCurrentTip(c => (c + 1) % tips.length), 6000);
    return () => clearInterval(iv);
  }, [tips.length]);

  const tip = tips[currentTip % tips.length];

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={currentTip}
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        className="mx-4 mb-3 px-3 py-2 rounded-lg border flex items-center gap-2"
        style={{ backgroundColor: `${tip.color}10`, borderColor: `${tip.color}30` }}
      >
        <Bell size={12} style={{ color: tip.color }} className="flex-shrink-0" />
        <p className="text-[10px] font-medium" style={{ color: tip.color }}>{tip.text}</p>
      </motion.div>
    </AnimatePresence>
  );
}

// 7. Streak Counter
function StreakCounter({ count, agent }) {
  if (count < 2) return null;
  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="mx-4 mb-3 px-3 py-2 rounded-xl bg-gradient-to-r from-[#F59E0B]/10 to-[#EF4444]/10 border border-[#F59E0B]/20 flex items-center justify-center gap-2"
    >
      <Flame size={14} className="text-[#F59E0B]" />
      <span className="text-xs font-bold text-white">{agent} is on a {count}-deal closing streak!</span>
      <span className="text-sm">{'🔥'.repeat(Math.min(count, 5))}</span>
    </motion.div>
  );
}

// 8. Weekly Leaderboard
function WeeklyLeaderboard({ data }) {
  return (
    <div className="px-4 mb-4">
      <h2 className="text-xs font-bold text-white mb-2 flex items-center gap-1.5">
        <Award size={12} className="text-[#D4AF37]" /> LEADERBOARD
      </h2>
      <div className="rounded-xl bg-[#0D1F35] border border-[#D4AF37]/10 overflow-hidden">
        {/* Header */}
        <div className="grid grid-cols-5 gap-1 px-3 py-2 border-b border-white/5">
          <span className="text-[8px] text-white/30 uppercase">Rank</span>
          <span className="text-[8px] text-white/30 uppercase">Agent</span>
          <span className="text-[8px] text-white/30 uppercase text-center">Close %</span>
          <span className="text-[8px] text-white/30 uppercase text-center">Revenue</span>
          <span className="text-[8px] text-white/30 uppercase text-center">Quality</span>
        </div>
        {/* Row */}
        <motion.div
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className="grid grid-cols-5 gap-1 px-3 py-2.5 items-center bg-gradient-to-r from-[#D4AF37]/5 to-transparent"
          style={{ animation: 'aegis-glow 3s ease-in-out infinite' }}
        >
          <div className="flex items-center gap-1">
            <span className="text-xs font-bold text-[#D4AF37]">#1</span>
            <span className="text-[8px]">{'🏆'}</span>
          </div>
          <span className="text-[10px] font-semibold text-white">{data.agent}</span>
          <span className="text-[10px] font-bold text-[#10B981] text-center">{data.closeRate}%</span>
          <span className="text-[10px] font-bold text-[#D4AF37] text-center">${data.revenue}</span>
          <div className="flex items-center justify-center gap-1">
            <span className="text-[10px] font-bold text-[#06B6D4]">{data.qualityScore}</span>
            <div className="w-8 h-1.5 rounded-full bg-[#1E3A5F] overflow-hidden">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-[#06B6D4] to-[#10B981]"
                initial={{ width: 0 }}
                animate={{ width: `${data.qualityScore}%` }}
                transition={{ duration: 1, delay: 0.5 }}
              />
            </div>
          </div>
        </motion.div>
        {/* Empty slots */}
        {[2, 3].map(rank => (
          <div key={rank} className="grid grid-cols-5 gap-1 px-3 py-2 items-center border-t border-white/5 opacity-20">
            <span className="text-[10px] text-white/30">#{rank}</span>
            <span className="text-[10px] text-white/20 italic">Available</span>
            <span className="text-[10px] text-white/20 text-center">—</span>
            <span className="text-[10px] text-white/20 text-center">—</span>
            <span className="text-[10px] text-white/20 text-center">—</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// 9. Call Script Panel (slide-up from FAB)
function CallScriptPanel({ isOpen, onClose }) {
  const [activeScript, setActiveScript] = useState(null);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 z-40"
            onClick={onClose}
          />
          {/* Panel */}
          <motion.div
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed bottom-0 left-0 right-0 z-50 bg-[#0D1F35] rounded-t-3xl border-t border-[#D4AF37]/20 max-h-[75vh] overflow-y-auto"
          >
            {/* Handle */}
            <div className="flex justify-center pt-3 pb-2">
              <div className="w-10 h-1 rounded-full bg-white/20" />
            </div>
            <div className="px-4 pb-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <FileText size={14} className="text-[#D4AF37]" />
                  Quick Call Scripts
                </h3>
                <button onClick={onClose} className="w-7 h-7 rounded-full bg-white/5 flex items-center justify-center">
                  <X size={14} className="text-white/50" />
                </button>
              </div>

              {/* Script Categories */}
              <div className="flex flex-wrap gap-2 mb-4">
                {Object.entries(CALL_SCRIPTS).map(([key, script]) => (
                  <button
                    key={key}
                    onClick={() => setActiveScript(activeScript === key ? null : key)}
                    className={`px-3 py-1.5 rounded-full text-[10px] font-medium border transition-all ${
                      activeScript === key
                        ? 'border-[#D4AF37]/50 bg-[#D4AF37]/10 text-[#D4AF37]'
                        : 'border-white/10 bg-white/5 text-white/50'
                    }`}
                  >
                    {script.label}
                  </button>
                ))}
              </div>

              {/* Script Content */}
              <AnimatePresence mode="wait">
                {activeScript && CALL_SCRIPTS[activeScript] && (
                  <motion.div
                    key={activeScript}
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="space-y-2"
                  >
                    {CALL_SCRIPTS[activeScript].lines.map((line, i) => (
                      <motion.div
                        key={i}
                        initial={{ x: -10, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: i * 0.08 }}
                        className="p-3 rounded-lg border border-white/5 bg-white/5"
                      >
                        <div className="flex items-start gap-2">
                          <span className="text-[9px] font-bold text-[#D4AF37] mt-0.5">{i + 1}.</span>
                          <p className="text-[11px] text-white/80 leading-relaxed">{line}</p>
                        </div>
                      </motion.div>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>

              {!activeScript && (
                <p className="text-[10px] text-white/30 text-center py-4">Tap a category above to see scripts</p>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

// ═══════════════════════════════════════════════════════════════
// MAIN DASHBOARD
// ═══════════════════════════════════════════════════════════════

export default function AegisDashboard() {
  const [tab, setTab] = useState('today');
  const [showScripts, setShowScripts] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [celebrateIndex, setCelebrateIndex] = useState(null);
  const [liveData, setLiveData] = useState(null);

  // Fetch live data from Supabase, refresh every 30s
  useEffect(() => {
    let mounted = true;
    const load = async () => {
      try {
        const stats = await fetchAegisDashboardStats();
        if (mounted) setLiveData(stats);
      } catch (e) {
        console.warn('AEGIS live data fetch failed, using demo:', e.message);
      }
    };
    load();
    const interval = setInterval(load, 30000);
    return () => { mounted = false; clearInterval(interval); };
  }, []);

  // Merge live data with demo defaults so all fields exist
  const d = liveData ? {
    ...DEMO_DATA,
    ...liveData,
    today: { ...DEMO_DATA.today, ...(liveData.today || {}) },
    week: { ...DEMO_DATA.week, ...(liveData.week || {}) },
    month: { ...DEMO_DATA.month, ...(liveData.month || {}) },
    hotLeads: liveData.hotLeads?.length > 0 ? liveData.hotLeads : DEMO_DATA.hotLeads,
    recentActivity: liveData.recentActivity?.length > 0 ? liveData.recentActivity : DEMO_DATA.recentActivity,
    sourceBreakdown: liveData.sourceBreakdown?.length > 0 ? liveData.sourceBreakdown.map((s, i) => ({
      ...s,
      color: [AEGIS.cyan, AEGIS.green, AEGIS.gold, AEGIS.amber, AEGIS.navy][i % 5],
      cost: s.cost || 0,
    })) : DEMO_DATA.sourceBreakdown,
    weeklyTrend: DEMO_DATA.weeklyTrend,
  } : DEMO_DATA;

  // Inject keyframe styles once
  useEffect(() => {
    const existing = document.getElementById('aegis-keyframes');
    if (!existing) {
      const style = document.createElement('style');
      style.id = 'aegis-keyframes';
      style.textContent = CONFETTI_STYLES;
      document.head.appendChild(style);
    }
    return () => {
      const el = document.getElementById('aegis-keyframes');
      if (el) el.remove();
    };
  }, []);

  // Animated revenue counter
  const animatedRevenue = useAnimatedCounter(d.today.revenue, 1800, '$');

  // Simulate marking a deal closed -> confetti
  const triggerCelebration = useCallback((activityIndex) => {
    setCelebrateIndex(activityIndex);
    setShowConfetti(true);
  }, []);

  return (
    <div className="min-h-screen bg-[#050A12] pb-32">
      {/* Confetti overlay */}
      <ConfettiCelebration active={showConfetti} onDone={() => setShowConfetti(false)} />

      {/* ─── Earnings Ticker ─── */}
      <EarningsTicker todayRevenue={d.today.revenue} monthRevenue={d.month.revenue} />

      {/* ─── AEGIS Header ─── */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1E3A5F]/30 via-transparent to-[#D4AF37]/10" />
        <div className="absolute top-0 right-0 w-32 h-32 bg-[#1E3A5F]/20 rounded-full blur-3xl" />
        <div className="relative px-4 pt-6 pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#1E3A5F] to-[#2A4A70] flex items-center justify-center ring-1 ring-[#D4AF37]/30">
                <Shield size={20} className="text-[#D4AF37]" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-white tracking-wide">AEGIS</h1>
                <p className="text-[9px] text-[#D4AF37]/70 tracking-[0.2em]">LEAD INTELLIGENCE SYSTEM</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1 px-2 py-1 rounded-full bg-[#10B981]/10 border border-[#10B981]/20">
                <div className="w-1.5 h-1.5 rounded-full bg-[#10B981] animate-pulse" />
                <span className="text-[9px] text-[#10B981] font-medium">LIVE</span>
              </div>
            </div>
          </div>

          {/* DayDay greeting */}
          <div className="mt-3 p-3 rounded-xl bg-gradient-to-r from-[#1E3A5F]/20 to-transparent border border-[#1E3A5F]/20">
            <p className="text-xs text-white/60">Welcome back, <span className="text-white font-semibold">DayDay</span></p>
            <p className="text-sm text-white mt-0.5">You have <span className="text-[#D4AF37] font-bold">{d.today.hotQueue} hot leads</span> waiting right now.</p>
          </div>
        </div>
      </div>

      {/* ─── Smart Notifications ─── */}
      <SmartNotificationBanner leads={d.hotLeads} closeRate={d.today.closeRate} />

      {/* ─── Streak Counter ─── */}
      <StreakCounter count={d.streak.count} agent={d.streak.agent} />

      {/* ─── Revenue Hero + Daily Goal ─── */}
      <div className="px-4 mb-4">
        <motion.div
          initial={{ y: 10, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#1E3A5F] to-[#0D1F35] border border-[#D4AF37]/20 p-4"
        >
          <div className="absolute top-0 right-0 w-40 h-40 bg-[#D4AF37]/5 rounded-full blur-3xl" />
          <div className="relative flex items-center justify-between">
            {/* Left: Revenue */}
            <div className="flex-1">
              <p className="text-[9px] text-[#D4AF37]/70 uppercase tracking-widest">Today's Revenue</p>
              <div className="flex items-end gap-2 mt-1">
                <span className="text-4xl font-bold text-white">{animatedRevenue}</span>
                <span className="text-sm text-[#10B981] flex items-center gap-0.5 mb-1"><ArrowUpRight size={14} /> 23%</span>
              </div>
              <div className="grid grid-cols-4 gap-2 mt-3">
                <MiniMetric value={d.today.leadsReceived} label="Leads" icon={<Users size={10} />} />
                <MiniMetric value={d.today.closed} label="Closed" icon={<CheckCircle2 size={10} />} color="text-[#10B981]" />
                <MiniMetric value={`${d.today.closeRate}%`} label="Close Rate" icon={<Target size={10} />} color="text-[#D4AF37]" />
                <MiniMetric value={d.today.avgResponseTime} label="Avg Speed" icon={<Timer size={10} />} color="text-[#06B6D4]" />
              </div>
            </div>
            {/* Right: Daily Goal Ring */}
            <div className="ml-3">
              <DailyGoalRing closed={d.today.closed} goal={d.today.dailyGoal} />
            </div>
          </div>
        </motion.div>
      </div>

      {/* ─── Hot Lead Queue ─── */}
      <div className="px-4 mb-4">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xs font-bold text-white flex items-center gap-1.5">
            <Zap size={12} className="text-[#F59E0B]" /> HOT LEADS — CALL NOW
          </h2>
          <span className="text-[9px] text-[#EF4444] font-medium animate-pulse">{d.hotLeads.length} waiting</span>
        </div>
        <div className="space-y-2">
          {d.hotLeads.map((lead, i) => (
            <motion.div
              key={lead.id}
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: i * 0.1 }}
              className="rounded-xl bg-gradient-to-r from-[#1E3A5F]/30 to-[#0D1F35] border border-[#1E3A5F]/30 p-3 relative overflow-hidden"
            >
              {/* Urgency pulse bar */}
              <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-[#EF4444] to-[#F59E0B]" />
              <div className="pl-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {/* Lead Score Ring instead of plain circle */}
                    <LeadScoreRing score={lead.score} size={32} />
                    <div>
                      <p className="text-sm font-semibold text-white">{lead.name}</p>
                      <div className="flex items-center gap-2">
                        <span className="text-[9px] text-white/50">{lead.source}</span>
                        {/* Live Speed-to-Contact Timer */}
                        <SpeedTimer initialMinutes={lead.timeInQueue} />
                      </div>
                    </div>
                  </div>
                  <a href={`tel:${lead.phone.replace(/\D/g,'')}`} className="w-9 h-9 rounded-full bg-[#10B981] flex items-center justify-center shadow-lg shadow-[#10B981]/20 relative">
                    <Phone size={16} className="text-white" />
                    {/* Pulse ring on urgent leads */}
                    {lead.timeInQueue > 5 && (
                      <div className="absolute inset-0 rounded-full border-2 border-[#10B981]" style={{ animation: 'aegis-pulse-ring 1.5s ease-out infinite' }} />
                    )}
                  </a>
                </div>
                <p className="text-[10px] text-[#D4AF37] mt-1.5 font-medium">{lead.reason}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* ─── Performance Metrics ─── */}
      <div className="px-4 mb-4">
        <h2 className="text-xs font-bold text-white mb-2 flex items-center gap-1.5"><BarChart3 size={12} className="text-[#06B6D4]" /> PERFORMANCE</h2>

        {/* Tab Toggle */}
        <div className="flex gap-1 mb-3 bg-[#0D1F35] rounded-lg p-0.5">
          {['today', 'week', 'month'].map(t => (
            <button key={t} onClick={() => setTab(t)} className={`flex-1 py-1.5 rounded-md text-[10px] font-medium transition-all ${tab === t ? 'bg-[#1E3A5F] text-[#D4AF37]' : 'text-white/40'}`}>
              {t.toUpperCase()}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {tab === 'today' && (
            <motion.div key="today" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="grid grid-cols-2 gap-2">
              <StatCard label="Leads In" value={d.today.leadsReceived} icon={<Users size={14} />} color="text-[#06B6D4]" bg="from-[#06B6D4]/10" />
              <StatCard label="Contacted" value={d.today.leadsContacted} icon={<PhoneCall size={14} />} color="text-[#10B981]" bg="from-[#10B981]/10" subtitle={`${Math.round(d.today.leadsContacted/d.today.leadsReceived*100)}% contact rate`} />
              <StatCard label="Quotes Given" value={d.today.quotesGiven} icon={<Star size={14} />} color="text-[#F59E0B]" bg="from-[#F59E0B]/10" />
              <StatCard label="Deals Closed" value={d.today.closed} icon={<CheckCircle2 size={14} />} color="text-[#10B981]" bg="from-[#10B981]/10" subtitle={`$${d.today.revenue} earned`} />
            </motion.div>
          )}
          {tab === 'week' && (
            <motion.div key="week" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="grid grid-cols-2 gap-2 mb-3">
                <StatCard label="Total Leads" value={d.week.leadsReceived} icon={<Users size={14} />} color="text-[#06B6D4]" bg="from-[#06B6D4]/10" />
                <StatCard label="Closed" value={d.week.closed} icon={<CheckCircle2 size={14} />} color="text-[#10B981]" bg="from-[#10B981]/10" subtitle={`$${d.week.revenue.toLocaleString()}`} />
                <StatCard label="Cost/Lead" value={`$${d.week.costPerLead}`} icon={<DollarSign size={14} />} color="text-[#F59E0B]" bg="from-[#F59E0B]/10" />
                <StatCard label="Cost/Close" value={`$${d.week.costPerClose}`} icon={<Target size={14} />} color="text-[#D4AF37]" bg="from-[#D4AF37]/10" />
              </div>
              {/* Weekly Bar Chart */}
              <div className="rounded-xl bg-[#0D1F35] border border-[#1E3A5F]/20 p-3">
                <p className="text-[9px] text-white/40 uppercase tracking-wider mb-2">Daily Breakdown</p>
                <div className="flex items-end justify-between gap-1 h-20">
                  {d.weeklyTrend.map((day, i) => (
                    <div key={i} className="flex-1 flex flex-col items-center gap-1">
                      <div className="w-full flex flex-col items-center gap-0.5">
                        <div className="w-full rounded-t bg-[#D4AF37]/30" style={{ height: `${day.closes * 12}px` }} />
                        <div className="w-full rounded-t bg-[#1E3A5F]" style={{ height: `${day.leads * 3}px` }} />
                      </div>
                      <span className="text-[7px] text-white/30">{day.day}</span>
                    </div>
                  ))}
                </div>
                <div className="flex items-center gap-3 mt-2">
                  <span className="text-[8px] text-white/30 flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-[#1E3A5F]" /> Leads</span>
                  <span className="text-[8px] text-white/30 flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-[#D4AF37]/30" /> Closes</span>
                </div>
              </div>
            </motion.div>
          )}
          {tab === 'month' && (
            <motion.div key="month" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="grid grid-cols-2 gap-2 mb-3">
                <StatCard label="Total Leads" value={d.month.leadsReceived} icon={<Users size={14} />} color="text-[#06B6D4]" bg="from-[#06B6D4]/10" />
                <StatCard label="Closed" value={d.month.closed} icon={<CheckCircle2 size={14} />} color="text-[#10B981]" bg="from-[#10B981]/10" subtitle={`$${d.month.revenue.toLocaleString()}`} />
              </div>
              {/* ROI Hero */}
              <div className="rounded-xl bg-gradient-to-r from-[#10B981]/10 to-[#D4AF37]/10 border border-[#10B981]/20 p-4 mb-3">
                <p className="text-[9px] text-white/40 uppercase tracking-widest">Return on Ad Spend</p>
                <div className="flex items-end gap-2 mt-1">
                  <span className="text-4xl font-bold text-[#10B981]">{d.month.roi}%</span>
                  <span className="text-xs text-white/40 mb-1">ROI</span>
                </div>
                <div className="flex items-center justify-between mt-2 text-[10px]">
                  <span className="text-white/40">Ad Spend: <span className="text-white font-medium">${d.month.adSpend.toLocaleString()}</span></span>
                  <span className="text-white/40">Revenue: <span className="text-[#10B981] font-medium">${d.month.revenue.toLocaleString()}</span></span>
                </div>
              </div>
              {/* Projected Annual */}
              <div className="rounded-xl bg-[#0D1F35] border border-[#D4AF37]/10 p-3 text-center">
                <p className="text-[9px] text-[#D4AF37]/60 uppercase tracking-widest">Projected Annual Revenue</p>
                <p className="text-3xl font-bold text-[#D4AF37] mt-1">${(d.month.projectedAnnual/1000).toFixed(0)}K</p>
                <p className="text-[9px] text-white/30 mt-0.5">Based on current close rate and volume</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* ─── Weekly Leaderboard ─── */}
      <WeeklyLeaderboard data={d.leaderboard} />

      {/* ─── Source Performance ─── */}
      <div className="px-4 mb-4">
        <h2 className="text-xs font-bold text-white mb-2 flex items-center gap-1.5"><PieChart size={12} className="text-[#D4AF37]" /> LEAD SOURCES</h2>
        <div className="rounded-xl bg-[#0D1F35] border border-[#1E3A5F]/20 p-3">
          {d.sourceBreakdown.map((src, i) => (
            <div key={i} className={`flex items-center justify-between py-2 ${i < d.sourceBreakdown.length - 1 ? 'border-b border-white/5' : ''}`}>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: src.color }} />
                <span className="text-[10px] text-white/70">{src.name}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-[9px] text-white/30">{src.leads} leads</span>
                <span className="text-[9px] text-[#10B981]">{src.closes} closed</span>
                <span className="text-[9px] text-[#D4AF37] font-medium">{src.rate}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ─── Recent Activity Feed ─── */}
      <div className="px-4 mb-4">
        <h2 className="text-xs font-bold text-white mb-2 flex items-center gap-1.5"><Activity size={12} className="text-[#10B981]" /> LIVE ACTIVITY</h2>
        <div className="space-y-1.5">
          {d.recentActivity.map((act, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className={`rounded-lg bg-[#0D1F35]/60 border p-2.5 flex items-start gap-2.5 cursor-pointer transition-all ${
                celebrateIndex === i ? 'border-[#10B981]/40 bg-[#10B981]/5' : 'border-[#1E3A5F]/10'
              }`}
              onClick={() => act.type === 'close' && triggerCelebration(i)}
            >
              <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 ${
                act.type === 'close' ? 'bg-[#10B981]/20' :
                act.type === 'quote' ? 'bg-[#F59E0B]/20' :
                act.type === 'contact' ? 'bg-[#06B6D4]/20' :
                'bg-[#1E3A5F]/40'
              }`}>
                {act.type === 'close' ? <DollarSign size={12} className="text-[#10B981]" /> :
                 act.type === 'quote' ? <Star size={12} className="text-[#F59E0B]" /> :
                 act.type === 'contact' ? <PhoneCall size={12} className="text-[#06B6D4]" /> :
                 <Zap size={12} className="text-[#D4AF37]" />}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-medium text-white">{act.name}</span>
                  <span className="text-[8px] text-white/20">{act.time}</span>
                </div>
                <p className="text-[9px] text-white/40">{act.detail}</p>
                {act.type === 'close' && <p className="text-[7px] text-[#10B981]/50 mt-0.5">Tap to celebrate</p>}
              </div>
              {act.amount && <span className="text-[10px] font-bold text-[#10B981] flex-shrink-0">{act.amount}</span>}
            </motion.div>
          ))}
        </div>
      </div>

      {/* ─── Money Summary Card ─── */}
      <div className="px-4 mb-6">
        <div className="rounded-2xl bg-gradient-to-br from-[#D4AF37]/10 to-[#1E3A5F]/20 border border-[#D4AF37]/20 p-4">
          <p className="text-[9px] text-[#D4AF37]/60 uppercase tracking-widest text-center">Your Money This Month</p>
          <div className="grid grid-cols-3 gap-3 mt-3">
            <div className="text-center">
              <p className="text-lg font-bold text-[#10B981]">${(d.month.revenue).toLocaleString()}</p>
              <p className="text-[8px] text-white/30">Gross Revenue</p>
            </div>
            <div className="text-center">
              <p className="text-lg font-bold text-[#F59E0B]">-${(d.month.adSpend).toLocaleString()}</p>
              <p className="text-[8px] text-white/30">Ad Spend</p>
            </div>
            <div className="text-center">
              <p className="text-lg font-bold text-[#D4AF37]">${(d.month.revenue - d.month.adSpend).toLocaleString()}</p>
              <p className="text-[8px] text-white/30">Net Profit</p>
            </div>
          </div>
          <div className="mt-3 pt-3 border-t border-white/5 text-center">
            <p className="text-[9px] text-white/30">Commission earnings are separate — this tracks lead system revenue only</p>
          </div>
        </div>
      </div>

      {/* ─── Powered by footer ─── */}
      <div className="text-center pb-4">
        <p className="text-[8px] text-white/10 tracking-widest">POWERED BY SOULHUSTLE AI</p>
      </div>

      {/* ═══ Floating Action Buttons ═══ */}
      <div className="fixed bottom-6 right-6 z-30 flex flex-col gap-3">
        {/* Chat with AEGIS */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setShowChat(true)}
          className="w-14 h-14 rounded-full bg-gradient-to-br from-[#1E3A5F] to-[#0D1F35] border border-[#D4AF37]/30 shadow-lg shadow-[#1E3A5F]/30 flex items-center justify-center"
        >
          <Shield size={22} className="text-[#D4AF37]" />
        </motion.button>
        {/* Call Scripts */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setShowScripts(true)}
          className="w-14 h-14 rounded-full bg-gradient-to-br from-[#D4AF37] to-[#B8960C] shadow-lg shadow-[#D4AF37]/30 flex items-center justify-center"
          style={{ animation: 'aegis-glow 3s ease-in-out infinite' }}
        >
          <FileText size={22} className="text-[#050A12]" />
        </motion.button>
      </div>

      {/* ═══ Call Script Slide-up Panel ═══ */}
      <CallScriptPanel isOpen={showScripts} onClose={() => setShowScripts(false)} />

      {/* ═══ AEGIS Chat Panel ═══ */}
      <AegisChatPanel isOpen={showChat} onClose={() => setShowChat(false)} />
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// SHARED SUB-COMPONENTS
// ═══════════════════════════════════════════════════════════════

function MiniMetric({ value, label, icon, color = 'text-white' }) {
  return (
    <div className="text-center">
      <div className={`flex items-center justify-center gap-0.5 ${color}`}>{icon}<span className="text-sm font-bold">{value}</span></div>
      <p className="text-[7px] text-white/30 mt-0.5">{label}</p>
    </div>
  );
}

function StatCard({ label, value, icon, color, bg, subtitle }) {
  return (
    <div className={`rounded-xl bg-gradient-to-br ${bg} to-transparent border border-white/5 p-3`}>
      <div className="flex items-center gap-1.5 mb-1">
        <span className={color}>{icon}</span>
        <span className="text-[9px] text-white/40">{label}</span>
      </div>
      <p className={`text-xl font-bold ${color}`}>{value}</p>
      {subtitle && <p className="text-[8px] text-white/30 mt-0.5">{subtitle}</p>}
    </div>
  );
}

// ═══════════════════════════════════════════════════════════════
// AEGIS CHAT PANEL — DayDay talks to his AI CEO
// ═══════════════════════════════════════════════════════════════

const AEGIS_BRAIN = {
  name: 'AEGIS',
  role: 'Lead Intelligence CEO',
  personality: 'Strategic, direct, protective. Speaks like a military intelligence officer meets a Wall Street analyst. Always focused on lead quality, close rates, and protecting DayDay\'s pipeline. Uses data to back up everything. Calls DayDay "D" casually.',
  greeting: "What's good D? I'm monitoring your pipeline right now. 3 hot leads waiting — Marcus J. is the highest priority, lost his job 3 days ago. What do you need?",
  knowledge: [
    'Health insurance lead scoring and qualification',
    'ACA, Medicare, Medicaid, COBRA, Special Enrollment Periods',
    'Lead conversion tactics and objection handling',
    'Pipeline analytics and performance optimization',
    'Call scripting and discovery frameworks',
    'Insurance carrier products and plan comparisons',
    'Compliance (TCPA, CMS, state regulations)',
  ],
};

const AEGIS_RESPONSES = {
  leads: [
    "Your pipeline is healthy right now D. 12 leads today, 3 A-tier. Marcus J. is the one to call first — COBRA expiring, high urgency. Score: 94.",
    "I'm seeing strong signal from Facebook today. 22% close rate on that channel. Google is slightly higher at 26% but lower volume. I'd increase FB spend by $50 this week to test.",
    "You've got 3 leads sitting over 5 minutes. Speed to contact is everything D — every minute you wait, close probability drops 10%. Let's go.",
  ],
  money: [
    "Here's your money picture: $1,275 today off 3 closes. Average lead fee is $85. Your cost per lead is running $12.40 this week — that's a 689% ROI on ad spend. We're printing.",
    "Monthly projection based on current pace: $22K revenue, $2.8K ad spend, $19.3K net. And that's just the lead fees — your actual commissions on top are another $12-22K.",
    "Your best ROI channel is referrals — zero cost, 24% close rate. Every client you close, ask for 2 referrals. That's free pipeline D.",
  ],
  scripts: [
    "For the job loss lead, open with: 'Hey Marcus, this is DayDay. I know losing a job is stressful — I'm not here to add to that. I help people in exactly your situation figure out coverage before the gap gets expensive. Got 5 minutes?' — Direct, empathetic, no BS.",
    "For the pregnant lead: 'Tanya, congrats on the baby. I help expecting mothers make sure they have the right coverage before delivery. Have you looked into your options yet?' — Lead with care, pivot to urgency around delivery costs.",
    "When someone says 'I need to think about it' — 'I hear you. Just so you know, coverage gaps can cost you if anything happens between now and when you decide. What specifically do you want to think about?' — Don't let them off the hook, but don't push. Seek truth.",
  ],
  performance: [
    "Your close rate is 33% today which is fire. Industry average for health insurance is 15-20%. You're running laps around other agents D.",
    "One thing I noticed — your B-tier leads have a 12% close rate vs 48% on A-tier. That's normal but there's room. Try calling B-tier leads within 30 min instead of 2 hours.",
    "Your 3-deal streak is solid. Momentum matters in sales. The next call is always easier after a close. Keep that energy.",
  ],
  general: [
    "I'm always watching your pipeline D. Right now everything is green — leads flowing, close rate above average, speed to contact is solid. Just keep answering that phone.",
    "Remember — you don't need to sell insurance. You need to find out if someone has a problem and whether you can solve it. Discovery first, recommendation second.",
    "The system is getting smarter every day. Every lead you disposition helps me score future leads more accurately. The more data you give me, the better your pipeline gets.",
    "Think of me as your shield D — I filter the noise so you only talk to people who actually need help. No tire kickers, no fake numbers, no wasted calls.",
  ],
};

function getAegisResponse(msg) {
  const lower = msg.toLowerCase();
  if (lower.includes('lead') || lower.includes('pipeline') || lower.includes('queue') || lower.includes('who should i call')) {
    return AEGIS_RESPONSES.leads[Math.floor(Math.random() * AEGIS_RESPONSES.leads.length)];
  }
  if (lower.includes('money') || lower.includes('revenue') || lower.includes('roi') || lower.includes('profit') || lower.includes('cost') || lower.includes('earning')) {
    return AEGIS_RESPONSES.money[Math.floor(Math.random() * AEGIS_RESPONSES.money.length)];
  }
  if (lower.includes('script') || lower.includes('say') || lower.includes('open') || lower.includes('pitch') || lower.includes('objection') || lower.includes('call')) {
    return AEGIS_RESPONSES.scripts[Math.floor(Math.random() * AEGIS_RESPONSES.scripts.length)];
  }
  if (lower.includes('rate') || lower.includes('performance') || lower.includes('stats') || lower.includes('how am i') || lower.includes('doing')) {
    return AEGIS_RESPONSES.performance[Math.floor(Math.random() * AEGIS_RESPONSES.performance.length)];
  }
  return AEGIS_RESPONSES.general[Math.floor(Math.random() * AEGIS_RESPONSES.general.length)];
}

function AegisChatPanel({ isOpen, onClose }) {
  const [messages, setMessages] = useState([
    { from: 'aegis', text: AEGIS_BRAIN.greeting, time: new Date() },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const messagesEnd = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (isOpen) setTimeout(() => inputRef.current?.focus(), 300);
  }, [isOpen]);

  const send = () => {
    if (!input.trim()) return;
    const userMsg = input.trim();
    setMessages(prev => [...prev, { from: 'user', text: userMsg, time: new Date() }]);
    setInput('');
    setTyping(true);

    // Simulate AEGIS thinking (would connect to Claude API in production)
    const delay = 800 + Math.random() * 1200;
    setTimeout(() => {
      const response = getAegisResponse(userMsg);
      setMessages(prev => [...prev, { from: 'aegis', text: response, time: new Date() }]);
      setTyping(false);
    }, delay);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ y: '100%' }}
          animate={{ y: 0 }}
          exit={{ y: '100%' }}
          transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          className="fixed inset-0 z-50 bg-[#050A12] flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-[#1E3A5F]/30 bg-[#0D1F35]">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#1E3A5F] to-[#2A4A70] flex items-center justify-center ring-1 ring-[#D4AF37]/30">
                <Shield size={18} className="text-[#D4AF37]" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">AEGIS</h3>
                <div className="flex items-center gap-1">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#10B981] animate-pulse" />
                  <span className="text-[9px] text-[#10B981]">Online — Lead Intelligence CEO</span>
                </div>
              </div>
            </div>
            <button onClick={onClose} className="p-2 rounded-full hover:bg-white/5">
              <X size={18} className="text-white/50" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
            {messages.map((msg, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 ${
                  msg.from === 'user'
                    ? 'bg-[#1E3A5F] text-white rounded-br-sm'
                    : 'bg-[#0D1F35] border border-[#1E3A5F]/30 text-white/90 rounded-bl-sm'
                }`}>
                  {msg.from === 'aegis' && (
                    <div className="flex items-center gap-1 mb-1">
                      <Shield size={10} className="text-[#D4AF37]" />
                      <span className="text-[8px] text-[#D4AF37] font-medium">AEGIS</span>
                    </div>
                  )}
                  <p className="text-[11px] leading-relaxed">{msg.text}</p>
                  <p className="text-[7px] text-white/20 mt-1 text-right">
                    {msg.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </motion.div>
            ))}
            {typing && (
              <div className="flex items-center gap-2 px-3">
                <Shield size={10} className="text-[#D4AF37]" />
                <div className="flex gap-1">
                  {[0,1,2].map(i => (
                    <div key={i} className="w-1.5 h-1.5 rounded-full bg-[#D4AF37]/50" style={{ animation: `aegis-pulse-ring 1s ease-in-out ${i * 0.2}s infinite` }} />
                  ))}
                </div>
              </div>
            )}
            <div ref={messagesEnd} />
          </div>

          {/* Quick Actions */}
          <div className="px-4 py-2 flex gap-2 overflow-x-auto">
            {['Who should I call?', 'How am I doing?', 'Show me the money', 'Help with a script'].map(q => (
              <button key={q} onClick={() => { setInput(q); }} className="flex-shrink-0 px-3 py-1.5 rounded-full bg-[#1E3A5F]/30 border border-[#1E3A5F]/30 text-[9px] text-white/50 hover:text-[#D4AF37] hover:border-[#D4AF37]/30 transition-all">
                {q}
              </button>
            ))}
          </div>

          {/* Input */}
          <div className="px-4 py-3 border-t border-[#1E3A5F]/30 bg-[#0D1F35]">
            <div className="flex items-center gap-2">
              <input
                ref={inputRef}
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && send()}
                placeholder="Ask AEGIS anything..."
                className="flex-1 bg-[#050A12] border border-[#1E3A5F]/30 rounded-xl px-4 py-2.5 text-xs text-white placeholder-white/20 focus:outline-none focus:border-[#D4AF37]/50"
              />
              <button
                onClick={send}
                disabled={!input.trim()}
                className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#D4AF37] to-[#B8960C] flex items-center justify-center disabled:opacity-30"
              >
                <ChevronRight size={18} className="text-[#050A12]" />
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
