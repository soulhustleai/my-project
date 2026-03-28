import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Shield, Phone, TrendingUp, Users, Clock, DollarSign, Zap, ChevronRight,
  CheckCircle2, AlertCircle, ArrowUpRight, Star, PhoneCall, PhoneOff,
  PhoneMissed, Timer, Target, BarChart3, Activity, X, FileText, Award,
  Flame, ChevronUp, ChevronDown, Bell, MessageSquare, Send, Calendar,
  User, MapPin, Mail, Hash, Sparkles, ArrowRight, ArrowLeft, Eye,
  ChevronLeft, RotateCcw, Search, Filter, Globe, Mic, RefreshCw,
  Bookmark, Archive, Copy, ExternalLink, Bot, Table, Home, Layers,
  ArrowDown, ArrowUp, UserPlus, SkipForward
} from 'lucide-react';
import { createClient } from '@supabase/supabase-js';

// ─── Supabase Client ───
const supabase = createClient(
  'https://pjkurxtvvtxbpfearqhd.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqa3VyeHR2dnR4YnBmZWFycWhkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Mzk0ODM1MiwiZXhwIjoyMDg5NTI0MzUyfQ.0GFx9z3oo3oTQ-_0A9ml04wwTwHyCw1P0pyoDxyPizc'
);

// ─── Theme ───
const T = {
  bg: '#0A0A0A',
  surface: '#111111',
  card: '#161616',
  cardHover: '#1C1C1C',
  navy: '#1E3A5F',
  navyLight: '#2A4A70',
  navyDark: '#152D4A',
  gold: '#D4AF37',
  goldDim: 'rgba(212,175,55,0.15)',
  green: '#10B981',
  greenDim: 'rgba(16,185,129,0.15)',
  orange: '#FF8C00',
  orangeDim: 'rgba(255,140,0,0.15)',
  cyan: '#06B6D4',
  text: '#FFFFFF',
  textMuted: '#9CA3AF',
  textDim: '#6B7280',
  border: '#1F1F1F',
  borderLight: '#2A2A2A',
};

// ─── CSS Keyframes ───
const GLOBAL_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
@keyframes aegis-pulse { 0%,100% { opacity:0.4; } 50% { opacity:1; } }
@keyframes aegis-glow { 0%,100% { box-shadow:0 0 5px rgba(212,175,55,0.2); } 50% { box-shadow:0 0 25px rgba(212,175,55,0.5); } }
@keyframes aegis-ring { 0% { transform:scale(1);opacity:1; } 100% { transform:scale(2.5);opacity:0; } }
@keyframes aegis-shimmer { 0% { background-position:-200% 0; } 100% { background-position:200% 0; } }
@keyframes aegis-float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-6px); } }
@keyframes aegis-counter { from { opacity:0;transform:translateY(10px); } to { opacity:1;transform:translateY(0); } }
@keyframes aegis-streak { 0% { transform:scale(1); } 50% { transform:scale(1.15); } 100% { transform:scale(1); } }
.aegis-scroll::-webkit-scrollbar { width:4px; }
.aegis-scroll::-webkit-scrollbar-track { background:transparent; }
.aegis-scroll::-webkit-scrollbar-thumb { background:${T.navyDark};border-radius:4px; }
.aegis-scroll::-webkit-scrollbar-thumb:hover { background:${T.navy}; }
`;

// ─── Disposition Types ───
const DISPOSITIONS = [
  { key: 'medicaid', label: 'Medicaid', icon: '🏥', color: T.textDim, desc: "Can't help" },
  { key: 'aca_transfer', label: 'ACA Transfer', icon: '🔄', color: T.cyan, desc: 'Referral bonus' },
  { key: 'pa_sold', label: 'P-A Sold', icon: '✅', color: T.green, desc: 'Private - Annuity' },
  { key: 'sa_sold', label: 'S-A Sold', icon: '✅', color: T.green, desc: 'Supplemental - Annuity' },
  { key: 'ha_sold', label: 'H-A Sold', icon: '✅', color: T.green, desc: 'Health - Annuity' },
  { key: 'callback', label: 'Callback', icon: '📅', color: T.gold, desc: 'Schedule follow-up' },
  { key: 'no_answer', label: 'No Answer', icon: '📵', color: T.orange, desc: 'Try again' },
  { key: 'never_contacted', label: 'Never Contact', icon: '🗃️', color: T.textDim, desc: '7d/21 attempts' },
];

// ─── Demo Leads ───
const DEMO_LEADS = [
  { id: 'demo-1', first_name: 'Marcus', last_name: 'Williams', phone: '+12125551234', email: 'marcus.w@gmail.com', zip_code: '10001', state: 'NY', situation: 'Self-employed, no coverage. Family of 3. Wife pregnant. Needs immediate coverage.', reason: 'Self-employed, pregnant wife, family of 3', source: 'facebook_ad', source_detail: 'FB Lead Form - Health Coverage', tier: 'A', score: 95, status: 'new', assigned_to: null, notes: [], dayday_notes: '', contact_attempts: 0, last_contacted_at: null, timezone: 'America/New_York', created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(), urgency_score: 95, contactability_score: 90, insurability_score: 85, monetization_score: 92, is_verified: true },
  { id: 'demo-2', first_name: 'Jasmine', last_name: 'Carter', phone: '+13105559876', email: 'j.carter@yahoo.com', zip_code: '90210', state: 'CA', situation: 'Lost job last month. COBRA ending. 2 kids under 10.', reason: 'Job loss, COBRA ending, 2 kids', source: 'facebook_ad', source_detail: 'FB Lead Form - Affordable Plans', tier: 'A', score: 92, status: 'new', assigned_to: null, notes: [], dayday_notes: '', contact_attempts: 0, last_contacted_at: null, timezone: 'America/Los_Angeles', created_at: new Date(Date.now() - 1000 * 60 * 12).toISOString(), urgency_score: 90, contactability_score: 88, insurability_score: 82, monetization_score: 90, is_verified: true },
  { id: 'demo-3', first_name: 'DeShawn', last_name: 'Thompson', phone: '+17735554567', email: 'deshawn.t@outlook.com', zip_code: '60601', state: 'IL', situation: 'Gig worker, DoorDash. No insurance ever. Back pain issues.', reason: 'Gig worker, no coverage, health issues', source: 'facebook_ad', source_detail: 'FB Lead Form - Gig Workers', tier: 'A', score: 88, status: 'new', assigned_to: null, notes: [], dayday_notes: '', contact_attempts: 1, last_contacted_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), timezone: 'America/Chicago', created_at: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString(), urgency_score: 85, contactability_score: 80, insurability_score: 78, monetization_score: 88, is_verified: false },
  { id: 'demo-4', first_name: 'Aaliyah', last_name: 'Robinson', phone: '+14045558765', email: 'aaliyah.r@gmail.com', zip_code: '30301', state: 'GA', situation: 'Starting new business. Current plan too expensive ($800/mo). Wants affordable options.', reason: 'New business, plan too expensive', source: 'google_ad', source_detail: 'Google Search - Health Insurance', tier: 'B', score: 78, status: 'contacted', assigned_to: 'DayDay', notes: [{ text: 'Left voicemail. Seemed interested per ad submission.', date: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), by: 'DayDay' }], dayday_notes: 'Left voicemail. Seemed interested per ad submission.', contact_attempts: 2, last_contacted_at: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), timezone: 'America/New_York', created_at: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString(), urgency_score: 70, contactability_score: 75, insurability_score: 80, monetization_score: 72, is_verified: true },
  { id: 'demo-5', first_name: 'Tyrone', last_name: 'Jackson', phone: '+12145553456', email: 'tjackson@gmail.com', zip_code: '75201', state: 'TX', situation: 'Recently divorced. Lost coverage through spouse. Type 2 diabetes.', reason: 'Divorce, lost spouse coverage, diabetes', source: 'paid_social', source_detail: 'TikTok Lead Form', tier: 'A', score: 90, status: 'new', assigned_to: null, notes: [], dayday_notes: '', contact_attempts: 0, last_contacted_at: null, timezone: 'America/Chicago', created_at: new Date(Date.now() - 1000 * 60 * 25).toISOString(), urgency_score: 92, contactability_score: 85, insurability_score: 75, monetization_score: 88, is_verified: true },
  { id: 'demo-6', first_name: 'Patricia', last_name: 'Nguyen', phone: '+12065557890', email: 'p.nguyen@live.com', zip_code: '98101', state: 'WA', situation: 'Part-time worker. Employer doesnt offer benefits. Healthy but needs preventive.', reason: 'Part-time, no employer benefits', source: 'scrape_reddit', source_detail: 'Reddit r/healthinsurance', tier: 'B', score: 65, status: 'new', assigned_to: null, notes: [], dayday_notes: '', contact_attempts: 0, last_contacted_at: null, timezone: 'America/Los_Angeles', created_at: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(), urgency_score: 55, contactability_score: 60, insurability_score: 85, monetization_score: 60, is_verified: false },
  { id: 'demo-7', first_name: 'Robert', last_name: 'Garcia', phone: '+17135552345', email: 'r.garcia55@gmail.com', zip_code: '77001', state: 'TX', situation: 'Small business owner. 5 employees. Looking for group plan options.', reason: 'Small biz owner, 5 employees, group plan', source: 'scrape_linkedin', source_detail: 'LinkedIn scrape - business owners', tier: 'A', score: 85, status: 'new', assigned_to: null, notes: [], dayday_notes: '', contact_attempts: 0, last_contacted_at: null, timezone: 'America/Chicago', created_at: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(), urgency_score: 80, contactability_score: 82, insurability_score: 88, monetization_score: 90, is_verified: true },
  { id: 'demo-8', first_name: 'Keisha', last_name: 'Brown', phone: '+13015556789', email: 'keisha.b@gmail.com', zip_code: '20001', state: 'DC', situation: 'Single mom, 2 kids. Currently on marketplace plan but premium went up 40%.', reason: 'Single mom, premium increase 40%', source: 'scrape_facebook', source_detail: 'FB Group scrape - Moms Need Help', tier: 'B', score: 72, status: 'new', assigned_to: null, notes: [], dayday_notes: '', contact_attempts: 0, last_contacted_at: null, timezone: 'America/New_York', created_at: new Date(Date.now() - 1000 * 60 * 60 * 18).toISOString(), urgency_score: 68, contactability_score: 70, insurability_score: 80, monetization_score: 65, is_verified: false },
];

// ─── Demo Stats ───
const DEMO_STATS = {
  revenue: 4275,
  closeRate: 33,
  speedToContact: 4.2,
  avgScore: 82,
  streak: 3,
  dailyGoal: { current: 3, target: 5 },
  leaderboard: [
    { name: 'DayDay', calls: 28, closed: 3, revenue: 2850 },
    { name: 'Lauren', calls: 22, closed: 2, revenue: 1425 },
  ],
  callbacks: [
    { name: 'Marcus Williams', time: '2:30 PM', date: 'Today' },
    { name: 'Aaliyah Robinson', time: '10:00 AM', date: 'Tomorrow' },
  ],
};

// ─── State timezone map ───
const STATE_TZ = {
  AL:'America/Chicago',AK:'America/Anchorage',AZ:'America/Phoenix',AR:'America/Chicago',
  CA:'America/Los_Angeles',CO:'America/Denver',CT:'America/New_York',DE:'America/New_York',
  DC:'America/New_York',FL:'America/New_York',GA:'America/New_York',HI:'Pacific/Honolulu',
  ID:'America/Boise',IL:'America/Chicago',IN:'America/Indiana/Indianapolis',IA:'America/Chicago',
  KS:'America/Chicago',KY:'America/New_York',LA:'America/Chicago',ME:'America/New_York',
  MD:'America/New_York',MA:'America/New_York',MI:'America/Detroit',MN:'America/Chicago',
  MS:'America/Chicago',MO:'America/Chicago',MT:'America/Denver',NE:'America/Chicago',
  NV:'America/Los_Angeles',NH:'America/New_York',NJ:'America/New_York',NM:'America/Denver',
  NY:'America/New_York',NC:'America/New_York',ND:'America/Chicago',OH:'America/New_York',
  OK:'America/Chicago',OR:'America/Los_Angeles',PA:'America/New_York',RI:'America/New_York',
  SC:'America/New_York',SD:'America/Chicago',TN:'America/Chicago',TX:'America/Chicago',
  UT:'America/Denver',VT:'America/New_York',VA:'America/New_York',WA:'America/Los_Angeles',
  WV:'America/New_York',WI:'America/Chicago',WY:'America/Denver',
};

// ─── Helpers ───
function timeAgo(dateStr) {
  if (!dateStr) return 'Never';
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

function formatPhone(phone) {
  if (!phone) return '';
  const digits = phone.replace(/\D/g, '');
  if (digits.length === 11 && digits[0] === '1') {
    return `(${digits.slice(1,4)}) ${digits.slice(4,7)}-${digits.slice(7)}`;
  }
  if (digits.length === 10) {
    return `(${digits.slice(0,3)}) ${digits.slice(3,6)}-${digits.slice(6)}`;
  }
  return phone;
}

function getTierColor(tier) {
  if (tier === 'A') return T.green;
  if (tier === 'B') return T.gold;
  if (tier === 'C') return T.orange;
  return T.textDim;
}

function getTimezoneAbbr(tz) {
  try {
    return new Intl.DateTimeFormat('en-US', { timeZone: tz, timeZoneName: 'short' }).formatToParts(new Date()).find(p => p.type === 'timeZoneName')?.value || tz;
  } catch { return 'EST'; }
}

function getLeadTimezone(lead) {
  if (lead.timezone) return lead.timezone;
  if (lead.state && STATE_TZ[lead.state]) return STATE_TZ[lead.state];
  return 'America/New_York';
}

function getLocalHour(tz) {
  try {
    const formatter = new Intl.DateTimeFormat('en-US', { timeZone: tz, hour: 'numeric', hour12: false });
    return parseInt(formatter.format(new Date()));
  } catch { return 12; }
}

function getCallingStatus(tz) {
  const hour = getLocalHour(tz);
  if (hour >= 9 && hour < 20) return 'green';
  if ((hour >= 8 && hour < 9) || (hour >= 20 && hour < 21)) return 'yellow';
  return 'red';
}

function isCallingHours(tz) {
  try {
    const now = new Date();
    const formatter = new Intl.DateTimeFormat('en-US', { timeZone: tz, hour: 'numeric', hour12: false });
    const hour = parseInt(formatter.format(now));
    return hour >= 9 && hour < 21;
  } catch { return true; }
}

function getLocalTime(tz) {
  try {
    return new Intl.DateTimeFormat('en-US', { timeZone: tz, hour: 'numeric', minute: '2-digit', hour12: true }).format(new Date());
  } catch { return ''; }
}

function AnimatedCounter({ value, prefix = '', suffix = '', duration = 1500 }) {
  const [display, setDisplay] = useState(0);
  const ref = useRef(null);
  useEffect(() => {
    const start = display;
    const diff = value - start;
    if (diff === 0) return;
    const startTime = performance.now();
    const animate = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(start + diff * eased));
      if (progress < 1) ref.current = requestAnimationFrame(animate);
    };
    ref.current = requestAnimationFrame(animate);
    return () => ref.current && cancelAnimationFrame(ref.current);
  }, [value]);
  return <span>{prefix}{display.toLocaleString()}{suffix}</span>;
}

// ─── SCORE RING COMPONENT ───
function ScoreRing({ score, size = 56, strokeWidth = 4 }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;
  const color = score >= 80 ? T.green : score >= 60 ? T.gold : T.orange;
  return (
    <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
      <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke={T.border} strokeWidth={strokeWidth} />
      <motion.circle
        cx={size/2} cy={size/2} r={radius} fill="none" stroke={color} strokeWidth={strokeWidth}
        strokeLinecap="round" strokeDasharray={circumference}
        initial={{ strokeDashoffset: circumference }}
        animate={{ strokeDashoffset: circumference - progress }}
        transition={{ duration: 1, ease: 'easeOut' }}
      />
      <text x={size/2} y={size/2} textAnchor="middle" dominantBaseline="central"
        fill={color} fontSize={size * 0.28} fontWeight="700" fontFamily="Inter"
        style={{ transform: 'rotate(90deg)', transformOrigin: 'center' }}>
        {score}
      </text>
    </svg>
  );
}

// ─── SCORE BAR COMPONENT ───
function ScoreBar({ label, value, max = 100, color }) {
  const pct = Math.min((value / max) * 100, 100);
  return (
    <div style={{ marginBottom: 6 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
        <span style={{ fontSize: 10, color: T.textMuted, textTransform: 'uppercase', letterSpacing: 0.5 }}>{label}</span>
        <span style={{ fontSize: 10, color, fontWeight: 700 }}>{value}</span>
      </div>
      <div style={{ width: '100%', height: 5, borderRadius: 3, background: T.surface }}>
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          style={{ height: '100%', borderRadius: 3, background: color }}
        />
      </div>
    </div>
  );
}

// ─── MAIN COMPONENT ───
export default function AegisDashboard() {
  // ─── State ───
  const [mainTab, setMainTab] = useState('home'); // home | leads | pipeline
  const [leadsSubTab, setLeadsSubTab] = useState('all'); // ads | scrapes | all
  const [queueMode, setQueueMode] = useState('my'); // my | lauren
  const [currentUser] = useState('DayDay');
  const [leads, setLeads] = useState(DEMO_LEADS);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [noteText, setNoteText] = useState('');
  const [stats, setStats] = useState(DEMO_STATS);
  const [isLive, setIsLive] = useState(false);
  const [showComposer, setShowComposer] = useState(false);
  const [composerInput, setComposerInput] = useState('');
  const [composerOutput, setComposerOutput] = useState('');
  const [showHistory, setShowHistory] = useState(false);
  const [showCallbackModal, setShowCallbackModal] = useState(false);
  const [callbackDate, setCallbackDate] = useState('');
  const [callbackTime, setCallbackTime] = useState('');
  const [showDispositions, setShowDispositions] = useState(false);
  const [lastDisposition, setLastDisposition] = useState(null);
  const [showTextComposer, setShowTextComposer] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(0);
  const [templateText, setTemplateText] = useState('');
  const [copiedText, setCopiedText] = useState(false);
  // Pipeline state
  const [pipelineFilter, setPipelineFilter] = useState({ tier: 'all', status: 'all', source: 'all', assigned: 'all' });
  const [pipelineSort, setPipelineSort] = useState({ key: 'score', dir: 'desc' });
  const [expandedRow, setExpandedRow] = useState(null);
  const [pipelineSearch, setPipelineSearch] = useState('');
  const noteRef = useRef(null);

  // ─── Inject styles ───
  useEffect(() => {
    const id = 'aegis-styles';
    if (!document.getElementById(id)) {
      const style = document.createElement('style');
      style.id = id;
      style.textContent = GLOBAL_STYLES;
      document.head.appendChild(style);
    }
  }, []);

  // ─── Fetch LIVE data from Supabase ───
  useEffect(() => {
    async function fetchLiveLeads() {
      try {
        const { data, error } = await supabase
          .from('aegis_leads')
          .select('*')
          .order('score', { ascending: false });
        if (!error && data && data.length > 0) {
          const mapped = data.map(l => ({
            ...l,
            notes: l.notes || [],
            contact_attempts: l.contact_attempts || 0,
            dayday_notes: l.dayday_notes || '',
          }));
          setLeads(mapped);
          setIsLive(true);
        }
      } catch (e) { console.log('Using demo data:', e.message); }
    }
    async function fetchLiveStats() {
      try {
        const { data: allLeads } = await supabase.from('aegis_leads').select('*');
        const { data: revenue } = await supabase.from('aegis_revenue').select('*');
        if (allLeads && allLeads.length > 0) {
          const closed = allLeads.filter(l => l.status === 'closed' || l.status === 'sold').length;
          const contacted = allLeads.filter(l => ['contacted','quoted','closed','sold'].includes(l.status)).length;
          const totalRev = (revenue || []).reduce((s, r) => s + (r.amount || 0), 0);
          setStats(prev => ({
            ...prev,
            totalLeads: allLeads.length,
            closedDeals: closed,
            closeRate: contacted > 0 ? Math.round((closed / contacted) * 100) : 0,
            revenue: totalRev || prev.revenue,
            newToday: allLeads.filter(l => new Date(l.created_at).toDateString() === new Date().toDateString()).length,
          }));
        }
      } catch (e) { console.log('Stats fallback:', e.message); }
    }
    fetchLiveLeads();
    fetchLiveStats();
    const interval = setInterval(() => { fetchLiveLeads(); fetchLiveStats(); }, 30000);
    return () => clearInterval(interval);
  }, []);

  // ─── Determine source type ───
  function isAdSource(source) {
    if (!source) return false;
    return source.startsWith('facebook') || source.startsWith('google') || source.startsWith('paid') || source === 'tiktok_ad';
  }
  function isScrapeSource(source) {
    if (!source) return false;
    return source.startsWith('scrape');
  }

  // ─── LEADS tab: Filtered Leads ───
  const leadsFiltered = useMemo(() => {
    let pool = leads.filter(l => {
      // Exclude fully dispositioned leads from active queue
      if (['sold','disposed','transferred','archived'].includes(l.status)) return false;
      // Sub-tab filter
      if (leadsSubTab === 'ads') return isAdSource(l.source);
      if (leadsSubTab === 'scrapes') return isScrapeSource(l.source);
      return true; // all
    });
    // Queue filter
    if (queueMode === 'my') {
      pool = pool.filter(l => !l.assigned_to || l.assigned_to === currentUser);
    } else {
      pool = pool.filter(l => l.assigned_to === 'Lauren');
    }
    // Calling hours sort: callable leads float to top
    pool.sort((a, b) => {
      const aTz = getLeadTimezone(a);
      const bTz = getLeadTimezone(b);
      const aCallable = getCallingStatus(aTz) === 'green' ? 0 : getCallingStatus(aTz) === 'yellow' ? 1 : 2;
      const bCallable = getCallingStatus(bTz) === 'green' ? 0 : getCallingStatus(bTz) === 'yellow' ? 1 : 2;
      if (aCallable !== bCallable) return aCallable - bCallable;
      // Then tier: A < B < C
      if (a.tier !== b.tier) return a.tier < b.tier ? -1 : 1;
      // Then oldest first within same tier
      return new Date(a.created_at) - new Date(b.created_at);
    });
    return pool;
  }, [leads, leadsSubTab, queueMode, currentUser]);

  const currentLead = leadsFiltered[currentIndex] || null;

  // ─── Counts for sub-tabs ───
  const adsCount = useMemo(() => leads.filter(l => isAdSource(l.source) && !['sold','disposed','transferred','archived'].includes(l.status)).length, [leads]);
  const scrapesCount = useMemo(() => leads.filter(l => isScrapeSource(l.source) && !['sold','disposed','transferred','archived'].includes(l.status)).length, [leads]);

  // ─── Actions ───
  const goNext = useCallback(() => {
    setCurrentIndex(i => Math.min(i + 1, leadsFiltered.length - 1));
    setNoteText('');
    setShowHistory(false);
    setShowDispositions(false);
    setLastDisposition(null);
    setShowTextComposer(false);
  }, [leadsFiltered.length]);

  const goPrev = useCallback(() => {
    setCurrentIndex(i => Math.max(i - 1, 0));
    setNoteText('');
    setShowHistory(false);
    setShowDispositions(false);
    setShowTextComposer(false);
  }, []);

  const skipToBottom = useCallback(() => {
    // Move current lead to end of queue (conceptually skip)
    goNext();
  }, [goNext]);

  const saveNote = useCallback(() => {
    if (!noteText.trim() || !currentLead) return;
    const newNotes = [...(currentLead.notes || []), { text: noteText.trim(), date: new Date().toISOString(), by: currentUser }];
    const newDaydayNotes = (currentLead.dayday_notes ? currentLead.dayday_notes + '\n' : '') + noteText.trim();
    setLeads(prev => prev.map(l => l.id === currentLead.id ? {
      ...l,
      notes: newNotes,
      dayday_notes: newDaydayNotes,
    } : l));
    // Write to Supabase
    if (isLive && currentLead.id && !currentLead.id.startsWith('demo')) {
      supabase.from('aegis_leads').update({
        dayday_notes: newDaydayNotes,
      }).eq('id', currentLead.id).then(() => console.log('Notes saved'));
    }
    setNoteText('');
    if (noteRef.current) noteRef.current.focus();
  }, [noteText, currentLead, currentUser, isLive]);

  const handleDisposition = useCallback((disp) => {
    if (!currentLead) return;
    if (disp.key === 'callback') {
      setShowCallbackModal(true);
      return;
    }
    const newStatus = ['pa_sold', 'sa_sold', 'ha_sold'].includes(disp.key) ? 'sold'
      : disp.key === 'medicaid' ? 'disposed'
      : disp.key === 'aca_transfer' ? 'transferred'
      : disp.key === 'never_contacted' ? 'archived'
      : disp.key === 'no_answer' ? 'no_answer'
      : 'contacted';

    const updatedLead = {
      ...currentLead,
      status: newStatus,
      assigned_to: currentUser,
      contact_attempts: currentLead.contact_attempts + 1,
      last_contacted_at: new Date().toISOString(),
      notes: [...(currentLead.notes || []), { text: `Disposition: ${disp.label}`, date: new Date().toISOString(), by: currentUser }]
    };

    setLeads(prev => prev.map(l => l.id === currentLead.id ? updatedLead : l));

    // Write to Supabase
    if (isLive && currentLead.id && !currentLead.id.startsWith('demo')) {
      supabase.from('aegis_leads').update({
        status: newStatus,
        assigned_to: currentUser,
        contact_attempts: updatedLead.contact_attempts,
        dayday_notes: updatedLead.dayday_notes,
      }).eq('id', currentLead.id).then(() => console.log('Lead updated in Supabase'));
      // Log activity
      supabase.from('aegis_activity_log').insert({
        lead_id: currentLead.id,
        action: disp.key,
        description: `${currentUser}: ${disp.label} — ${currentLead.first_name} ${currentLead.last_name}`,
        created_by: currentUser.toLowerCase(),
      }).then(() => console.log('Activity logged'));
      // Log revenue for sold dispositions
      if (['pa_sold', 'sa_sold', 'ha_sold'].includes(disp.key)) {
        supabase.from('aegis_revenue').insert({
          lead_id: currentLead.id,
          type: 'close_fee',
          amount: currentLead.tier === 'A' ? 100 : 75,
          description: `${disp.label} — ${currentLead.first_name} ${currentLead.last_name}`,
          paid: false,
        }).then(() => console.log('Revenue logged'));
      }
    }

    setLastDisposition(disp);
    setShowDispositions(false);
    setTimeout(goNext, 800);
  }, [currentLead, currentUser, goNext, isLive]);

  const handleCallbackSchedule = useCallback(() => {
    if (!callbackDate || !callbackTime || !currentLead) return;
    setLeads(prev => prev.map(l => l.id === currentLead.id ? {
      ...l,
      status: 'callback',
      assigned_to: currentUser,
      notes: [...(l.notes || []), { text: `Callback scheduled: ${callbackDate} at ${callbackTime}`, date: new Date().toISOString(), by: currentUser }]
    } : l));
    setShowCallbackModal(false);
    setCallbackDate('');
    setCallbackTime('');
    setLastDisposition(DISPOSITIONS.find(d => d.key === 'callback'));
    setTimeout(goNext, 800);
  }, [callbackDate, callbackTime, currentLead, currentUser, goNext]);

  const sendToLauren = useCallback(() => {
    if (!currentLead) return;
    setLeads(prev => prev.map(l => l.id === currentLead.id ? { ...l, assigned_to: 'Lauren' } : l));
    if (isLive && currentLead.id && !currentLead.id.startsWith('demo')) {
      supabase.from('aegis_leads').update({ assigned_to: 'Lauren' }).eq('id', currentLead.id);
      supabase.from('aegis_activity_log').insert({
        lead_id: currentLead.id, action: 'reassign', description: `Reassigned to Lauren by ${currentUser}`, created_by: currentUser.toLowerCase(),
      });
    }
    goNext();
  }, [currentLead, currentUser, goNext, isLive]);

  // Text templates
  const TEXT_TEMPLATES = useMemo(() => {
    const name = currentLead?.first_name || 'there';
    return [
      { label: 'First Contact', text: `Hey ${name}, this is DayDay. I just reviewed what you sent through about health coverage. I specialize in finding plans that actually fit your budget. Got 2 min to chat today?` },
      { label: 'Follow-up', text: `Hey ${name}, just following up on your health coverage situation. I found some great options I think you'd really like. When's a good time for a quick call?` },
      { label: 'Hail Mary', text: `Hey ${name}, I found the most affordable option for your situation and wanted to make sure you saw it before enrollment closes. Can I call you real quick?` },
    ];
  }, [currentLead]);

  useEffect(() => {
    if (showTextComposer && TEXT_TEMPLATES.length > 0) {
      setTemplateText(TEXT_TEMPLATES[selectedTemplate]?.text || '');
    }
  }, [showTextComposer, selectedTemplate, TEXT_TEMPLATES]);

  const handleComposerRewrite = () => {
    if (!composerInput.trim()) return;
    const templates = [
      `Hi [Name], this is ${currentUser} with Godfident Insurance Solutions. I noticed you were looking into health coverage options. I'd love to help you find the best plan for your situation. When's a good time to chat for 5 minutes?`,
      `Hey [Name]! ${currentUser} here from Godfident. I saw you're exploring health insurance options. I specialize in finding affordable coverage that actually works. Got 5 minutes today?`,
      `[Name], ${currentUser} with Godfident Insurance. I help people just like you find affordable health coverage. I'd love to walk you through some options that could save you money. Free to chat today?`,
    ];
    setComposerOutput(templates[Math.floor(Math.random() * templates.length)].replace('[Name]', currentLead?.first_name || 'there'));
  };

  // ─── Contact rules ───
  const maxTotalAttempts = 21;
  const maxDays = 7;

  const contactRules = currentLead ? {
    attempts: currentLead.contact_attempts || 0,
    maxAttempts: maxTotalAttempts,
    daysSinceCreated: Math.floor((Date.now() - new Date(currentLead.created_at).getTime()) / 86400000),
    maxDays,
    lastContacted: currentLead.last_contacted_at,
    tz: getLeadTimezone(currentLead),
    canCall: isCallingHours(getLeadTimezone(currentLead)),
    callingStatus: getCallingStatus(getLeadTimezone(currentLead)),
  } : null;

  // ─── PIPELINE: filtered & sorted leads ───
  const pipelineLeads = useMemo(() => {
    let pool = [...leads];
    // Search
    if (pipelineSearch.trim()) {
      const q = pipelineSearch.toLowerCase();
      pool = pool.filter(l =>
        (l.first_name + ' ' + l.last_name).toLowerCase().includes(q) ||
        l.phone?.includes(q) ||
        l.email?.toLowerCase().includes(q)
      );
    }
    // Filters
    if (pipelineFilter.tier !== 'all') pool = pool.filter(l => l.tier === pipelineFilter.tier);
    if (pipelineFilter.status !== 'all') pool = pool.filter(l => l.status === pipelineFilter.status);
    if (pipelineFilter.source !== 'all') {
      if (pipelineFilter.source === 'ads') pool = pool.filter(l => isAdSource(l.source));
      else pool = pool.filter(l => isScrapeSource(l.source));
    }
    if (pipelineFilter.assigned !== 'all') {
      if (pipelineFilter.assigned === 'unassigned') pool = pool.filter(l => !l.assigned_to);
      else pool = pool.filter(l => l.assigned_to === pipelineFilter.assigned);
    }
    // Sort
    pool.sort((a, b) => {
      let aVal, bVal;
      switch (pipelineSort.key) {
        case 'score': aVal = a.score || 0; bVal = b.score || 0; break;
        case 'name': aVal = (a.first_name + a.last_name).toLowerCase(); bVal = (b.first_name + b.last_name).toLowerCase(); break;
        case 'date': aVal = new Date(a.created_at).getTime(); bVal = new Date(b.created_at).getTime(); break;
        default: aVal = a.score || 0; bVal = b.score || 0;
      }
      if (typeof aVal === 'string') return pipelineSort.dir === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
      return pipelineSort.dir === 'asc' ? aVal - bVal : bVal - aVal;
    });
    return pool;
  }, [leads, pipelineFilter, pipelineSort, pipelineSearch]);

  // ─────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────
  return (
    <div style={{
      minHeight: '100vh', background: T.bg, color: T.text, fontFamily: "'Inter', sans-serif",
      paddingBottom: '100px', position: 'relative',
    }}>
      {/* ─── HEADER ─── */}
      <div style={{
        position: 'sticky', top: 0, zIndex: 50, background: 'linear-gradient(180deg, #0A0A0A 0%, rgba(10,10,10,0.95) 100%)',
        backdropFilter: 'blur(20px)', borderBottom: `1px solid ${T.border}`,
        padding: '12px 16px 0',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', maxWidth: 1400, margin: '0 auto', marginBottom: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{
              width: 36, height: 36, borderRadius: 10,
              background: `linear-gradient(135deg, ${T.navy}, ${T.navyLight})`,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: `0 0 20px ${T.navy}40`,
            }}>
              <Shield size={20} color={T.gold} />
            </div>
            <div>
              <h1 style={{ fontFamily: "'Cinzel', serif", fontSize: 18, fontWeight: 700, color: T.gold, lineHeight: 1.1, letterSpacing: 1 }}>
                AEGIS
              </h1>
              <p style={{ fontSize: 10, color: T.textMuted, letterSpacing: 0.5 }}>HEALTH INSURANCE COMMAND</p>
            </div>
          </div>
          {/* Live indicator */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div style={{
              width: 8, height: 8, borderRadius: '50%',
              background: isLive ? T.green : T.orange,
              animation: isLive ? 'aegis-pulse 2s infinite' : 'none',
            }} />
            <span style={{ fontSize: 10, color: isLive ? T.green : T.orange, fontWeight: 600 }}>
              {isLive ? 'LIVE' : 'DEMO'}
            </span>
          </div>
        </div>

        {/* ─── SEGMENTED TAB CONTROL ─── */}
        <div style={{
          display: 'flex', maxWidth: 1400, margin: '0 auto',
          background: T.surface, borderRadius: '10px 10px 0 0', padding: 3, gap: 3,
        }}>
          {[
            { key: 'home', label: 'HOME', icon: <Home size={14} /> },
            { key: 'leads', label: 'LEADS', icon: <Layers size={14} /> },
            { key: 'pipeline', label: 'PIPELINE', icon: <Table size={14} /> },
          ].map(tab => (
            <button key={tab.key} onClick={() => { setMainTab(tab.key); setCurrentIndex(0); }} style={{
              flex: 1, padding: '10px 8px', borderRadius: 8, border: 'none', cursor: 'pointer',
              background: mainTab === tab.key ? `linear-gradient(135deg, ${T.navy}, ${T.navyDark})` : 'transparent',
              color: mainTab === tab.key ? T.gold : T.textMuted,
              fontSize: 12, fontWeight: 700, letterSpacing: 1, fontFamily: "'Cinzel', serif",
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
              transition: 'all 0.2s',
              boxShadow: mainTab === tab.key ? `0 2px 10px ${T.navy}40` : 'none',
            }}>
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* ─── MAIN CONTENT ─── */}
      <div style={{ maxWidth: 1400, margin: '0 auto', padding: '12px 16px' }}>
        <AnimatePresence mode="wait">

          {/* ═══════════════════════════════════════════════ */}
          {/* ═══ HOME TAB (SACRED — DayDay approved) ═══ */}
          {/* ═══════════════════════════════════════════════ */}
          {mainTab === 'home' && (
            <motion.div key="home" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} transition={{ duration: 0.2 }}>
              {/* Revenue Hero */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                style={{
                  padding: '24px 20px', borderRadius: 16, marginBottom: 12,
                  background: `linear-gradient(135deg, ${T.navy}30, ${T.green}10)`,
                  border: `1px solid ${T.navy}40`,
                  textAlign: 'center',
                }}
              >
                <p style={{ fontSize: 11, color: T.textMuted, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 4 }}>Total Revenue</p>
                <h2 style={{
                  fontFamily: "'Cinzel', serif", fontSize: 40, fontWeight: 900,
                  color: T.green, lineHeight: 1,
                  animation: 'aegis-counter 0.5s ease-out',
                }}>
                  <AnimatedCounter value={stats.revenue} prefix="$" />
                </h2>
                <p style={{ fontSize: 12, color: T.textDim, marginTop: 4 }}>This week</p>
              </motion.div>

              {/* Stats Grid */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 10, marginBottom: 12 }}>
                {/* Close Rate */}
                <div style={{ padding: '16px', borderRadius: 12, background: T.card, border: `1px solid ${T.border}` }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                    <Target size={14} color={T.green} />
                    <span style={{ fontSize: 11, color: T.textDim, textTransform: 'uppercase' }}>Close Rate</span>
                  </div>
                  <p style={{ fontSize: 28, fontWeight: 800, color: T.green, fontFamily: "'Cinzel', serif" }}>
                    <AnimatedCounter value={stats.closeRate} suffix="%" />
                  </p>
                </div>

                {/* Speed to Contact */}
                <div style={{ padding: '16px', borderRadius: 12, background: T.card, border: `1px solid ${T.border}` }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                    <Zap size={14} color={T.gold} />
                    <span style={{ fontSize: 11, color: T.textDim, textTransform: 'uppercase' }}>Speed to Contact</span>
                  </div>
                  <p style={{ fontSize: 28, fontWeight: 800, color: T.gold, fontFamily: "'Cinzel', serif" }}>
                    {stats.speedToContact}<span style={{ fontSize: 14, color: T.textDim }}>min</span>
                  </p>
                </div>

                {/* Average Score */}
                <div style={{ padding: '16px', borderRadius: 12, background: T.card, border: `1px solid ${T.border}` }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                    <Star size={14} color={T.cyan} />
                    <span style={{ fontSize: 11, color: T.textDim, textTransform: 'uppercase' }}>Avg Lead Score</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <ScoreRing score={stats.avgScore} size={48} strokeWidth={3} />
                  </div>
                </div>

                {/* Streak */}
                <div style={{ padding: '16px', borderRadius: 12, background: T.card, border: `1px solid ${T.border}` }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                    <Flame size={14} color={T.orange} />
                    <span style={{ fontSize: 11, color: T.textDim, textTransform: 'uppercase' }}>Close Streak</span>
                  </div>
                  <p style={{
                    fontSize: 28, fontWeight: 800, color: T.orange, fontFamily: "'Cinzel', serif",
                    animation: 'aegis-streak 2s ease-in-out infinite',
                  }}>
                    {stats.streak} <span style={{ fontSize: 20 }}>🔥</span>
                  </p>
                </div>
              </div>

              {/* Daily Goal */}
              <div style={{
                padding: '16px', borderRadius: 12, background: T.card,
                border: `1px solid ${T.border}`, marginBottom: 12,
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <Award size={14} color={T.gold} />
                    <span style={{ fontSize: 13, fontWeight: 600, color: T.gold, fontFamily: "'Cinzel', serif" }}>DAILY GOAL</span>
                  </div>
                  <span style={{ fontSize: 13, fontWeight: 700, color: T.text }}>
                    {stats.dailyGoal.current}/{stats.dailyGoal.target} Closes
                  </span>
                </div>
                <div style={{
                  width: '100%', height: 10, borderRadius: 5, background: T.surface,
                  overflow: 'hidden',
                }}>
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(stats.dailyGoal.current / stats.dailyGoal.target) * 100}%` }}
                    transition={{ duration: 1, ease: 'easeOut' }}
                    style={{
                      height: '100%', borderRadius: 5,
                      background: `linear-gradient(90deg, ${T.gold}, ${T.green})`,
                      boxShadow: `0 0 10px ${T.gold}40`,
                    }}
                  />
                </div>
                <p style={{ fontSize: 11, color: T.textDim, marginTop: 6, textAlign: 'center' }}>
                  {stats.dailyGoal.target - stats.dailyGoal.current} more to hit target
                </p>
              </div>

              {/* Leaderboard */}
              <div style={{
                padding: '16px', borderRadius: 12, background: T.card,
                border: `1px solid ${T.border}`, marginBottom: 12,
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 12 }}>
                  <TrendingUp size={14} color={T.gold} />
                  <span style={{ fontSize: 13, fontWeight: 600, color: T.gold, fontFamily: "'Cinzel', serif" }}>WEEKLY LEADERBOARD</span>
                </div>
                {stats.leaderboard.map((person, i) => (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '12px', borderRadius: 10,
                    background: i === 0 ? T.goldDim : T.surface,
                    border: `1px solid ${i === 0 ? T.gold + '30' : T.border}`,
                    marginBottom: i < stats.leaderboard.length - 1 ? 8 : 0,
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <span style={{
                        width: 28, height: 28, borderRadius: '50%',
                        background: i === 0 ? T.gold : T.navy,
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 12, fontWeight: 800, color: i === 0 ? T.bg : T.text,
                      }}>
                        {i + 1}
                      </span>
                      <div>
                        <p style={{ fontSize: 14, fontWeight: 700, color: T.text }}>{person.name}</p>
                        <p style={{ fontSize: 11, color: T.textDim }}>{person.calls} calls &bull; {person.closed} closed</p>
                      </div>
                    </div>
                    <span style={{
                      fontSize: 16, fontWeight: 800,
                      color: T.green, fontFamily: "'Cinzel', serif",
                    }}>
                      ${person.revenue.toLocaleString()}
                    </span>
                  </div>
                ))}
              </div>

              {/* Hot Lead Queue Preview */}
              <div style={{
                padding: '16px', borderRadius: 12, background: T.card,
                border: `1px solid ${T.border}`, marginBottom: 12,
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <Zap size={14} color={T.gold} />
                    <span style={{ fontSize: 13, fontWeight: 600, color: T.gold, fontFamily: "'Cinzel', serif" }}>HOT LEADS</span>
                  </div>
                  <button onClick={() => setMainTab('leads')} style={{
                    padding: '4px 10px', borderRadius: 6, border: `1px solid ${T.navy}`,
                    background: T.navyDark, color: T.gold, cursor: 'pointer', fontSize: 10, fontWeight: 600,
                    display: 'flex', alignItems: 'center', gap: 4,
                  }}>
                    View All <ArrowRight size={10} />
                  </button>
                </div>
                {leads.filter(l => l.tier === 'A' && !['sold','disposed','transferred','archived'].includes(l.status)).slice(0, 3).map((lead, i) => (
                  <div key={lead.id} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '10px 12px', borderRadius: 8, background: T.surface,
                    border: `1px solid ${T.border}`,
                    marginBottom: i < 2 ? 6 : 0,
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{
                        padding: '2px 6px', borderRadius: 4,
                        background: T.greenDim, color: T.green,
                        fontSize: 10, fontWeight: 800,
                      }}>A</span>
                      <div>
                        <p style={{ fontSize: 13, fontWeight: 600, color: T.text }}>{lead.first_name} {lead.last_name}</p>
                        <p style={{ fontSize: 11, color: T.textDim }}>{lead.reason || lead.situation?.slice(0, 40)}</p>
                      </div>
                    </div>
                    <ScoreRing score={lead.score} size={32} strokeWidth={2} />
                  </div>
                ))}
              </div>

              {/* Scheduled Callbacks */}
              <div style={{
                padding: '16px', borderRadius: 12, background: T.card,
                border: `1px solid ${T.border}`,
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 12 }}>
                  <Calendar size={14} color={T.gold} />
                  <span style={{ fontSize: 13, fontWeight: 600, color: T.gold, fontFamily: "'Cinzel', serif" }}>SCHEDULED CALLBACKS</span>
                </div>
                {stats.callbacks.length === 0 ? (
                  <p style={{ fontSize: 12, color: T.textDim, textAlign: 'center', padding: '16px 0' }}>No callbacks scheduled</p>
                ) : stats.callbacks.map((cb, i) => (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '10px 12px', borderRadius: 8, background: T.surface,
                    border: `1px solid ${T.border}`,
                    marginBottom: i < stats.callbacks.length - 1 ? 6 : 0,
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div style={{
                        width: 32, height: 32, borderRadius: 8,
                        background: T.goldDim, display: 'flex', alignItems: 'center', justifyContent: 'center',
                      }}>
                        <Phone size={14} color={T.gold} />
                      </div>
                      <div>
                        <p style={{ fontSize: 13, fontWeight: 600, color: T.text }}>{cb.name}</p>
                        <p style={{ fontSize: 11, color: T.textDim }}>{cb.date} at {cb.time}</p>
                      </div>
                    </div>
                    <button style={{
                      padding: '6px 12px', borderRadius: 6, border: `1px solid ${T.navy}`,
                      background: T.navyDark, color: T.text, cursor: 'pointer',
                      fontSize: 11, fontWeight: 600,
                    }}>
                      Call
                    </button>
                  </div>
                ))}
              </div>

              {/* Smart Notification */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                style={{
                  marginTop: 12, padding: '12px 16px', borderRadius: 12,
                  background: T.goldDim, border: `1px solid ${T.gold}30`,
                  display: 'flex', alignItems: 'center', gap: 10,
                }}
              >
                <Bell size={16} color={T.gold} />
                <div>
                  <p style={{ fontSize: 12, fontWeight: 600, color: T.gold }}>
                    {leads.filter(l => l.tier === 'A' && l.status === 'new').length} new A-tier leads waiting
                  </p>
                  <p style={{ fontSize: 11, color: T.textDim }}>Tap LEADS to start calling</p>
                </div>
              </motion.div>
            </motion.div>
          )}

          {/* ═══════════════════════════════════════════════ */}
          {/* ═══ LEADS TAB (Flash Card System) ═══ */}
          {/* ═══════════════════════════════════════════════ */}
          {mainTab === 'leads' && (
            <motion.div key="leads" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.2 }}>

              {/* Sub-tabs: ADS | SCRAPES | ALL */}
              <div style={{ display: 'flex', gap: 6, marginBottom: 10 }}>
                {[
                  { key: 'all', label: 'ALL', count: adsCount + scrapesCount },
                  { key: 'ads', label: 'ADS', count: adsCount, emoji: '🎯' },
                  { key: 'scrapes', label: 'SCRAPES', count: scrapesCount, emoji: '🕸️' },
                ].map(tab => (
                  <button key={tab.key} onClick={() => { setLeadsSubTab(tab.key); setCurrentIndex(0); }} style={{
                    flex: 1, padding: '8px 6px', borderRadius: 8,
                    border: `1px solid ${leadsSubTab === tab.key ? T.gold : T.border}`,
                    background: leadsSubTab === tab.key ? T.goldDim : T.surface,
                    cursor: 'pointer', textAlign: 'center', transition: 'all 0.2s',
                  }}>
                    <span style={{
                      fontSize: 11, fontWeight: 700, letterSpacing: 0.5,
                      color: leadsSubTab === tab.key ? T.gold : T.textMuted,
                    }}>
                      {tab.emoji ? tab.emoji + ' ' : ''}{tab.label}
                    </span>
                    <span style={{
                      display: 'block', fontSize: 10, color: T.textDim, marginTop: 2,
                    }}>({tab.count})</span>
                  </button>
                ))}
              </div>

              {/* Queue Toggle: DayDay / Lauren */}
              <div style={{ display: 'flex', gap: 6, marginBottom: 10 }}>
                {[
                  { key: 'my', label: "DayDay's Leads" },
                  { key: 'lauren', label: "Lauren's Leads" },
                ].map(q => (
                  <button key={q.key} onClick={() => { setQueueMode(q.key); setCurrentIndex(0); }} style={{
                    flex: 1, padding: '8px 10px', borderRadius: 8, border: 'none', cursor: 'pointer',
                    background: queueMode === q.key ? T.navyDark : T.surface,
                    color: queueMode === q.key ? T.text : T.textMuted,
                    fontSize: 12, fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
                    transition: 'all 0.2s',
                  }}>
                    <Users size={12} /> {q.label}
                  </button>
                ))}
              </div>

              {/* ─── FLASH CARD LEAD SYSTEM ─── */}
              {leadsFiltered.length === 0 ? (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ textAlign: 'center', padding: '60px 20px' }}>
                  <Shield size={64} color={T.navy} style={{ margin: '0 auto 16px', opacity: 0.3 }} />
                  <h2 style={{ fontFamily: "'Cinzel', serif", fontSize: 20, color: T.textMuted, marginBottom: 8 }}>Queue Empty</h2>
                  <p style={{ color: T.textDim, fontSize: 14 }}>
                    {leadsSubTab === 'ads' ? 'No ad leads in queue.' : leadsSubTab === 'scrapes' ? 'No scraped leads.' : 'No leads in queue.'}
                  </p>
                </motion.div>
              ) : currentLead ? (
                <div>
                  {/* Lead Counter */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
                    <span style={{ fontSize: 12, color: T.textDim }}>
                      Lead {currentIndex + 1} of {leadsFiltered.length}
                    </span>
                    <div style={{ display: 'flex', gap: 6 }}>
                      <button onClick={goPrev} disabled={currentIndex === 0} style={{
                        width: 32, height: 32, borderRadius: 8, border: `1px solid ${T.border}`,
                        background: T.surface, color: currentIndex === 0 ? T.textDim : T.text,
                        cursor: currentIndex === 0 ? 'not-allowed' : 'pointer',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: currentIndex === 0 ? 0.4 : 1,
                      }}>
                        <ChevronLeft size={16} />
                      </button>
                      <button onClick={goNext} disabled={currentIndex >= leadsFiltered.length - 1} style={{
                        width: 32, height: 32, borderRadius: 8, border: `1px solid ${T.border}`,
                        background: T.surface, color: currentIndex >= leadsFiltered.length - 1 ? T.textDim : T.text,
                        cursor: currentIndex >= leadsFiltered.length - 1 ? 'not-allowed' : 'pointer',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        opacity: currentIndex >= leadsFiltered.length - 1 ? 0.4 : 1,
                      }}>
                        <ChevronRight size={16} />
                      </button>
                    </div>
                  </div>

                  {/* Disposition Success Flash */}
                  <AnimatePresence>
                    {lastDisposition && (
                      <motion.div
                        initial={{ opacity: 0, y: -20, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -20 }}
                        style={{
                          padding: '12px 16px', borderRadius: 12, marginBottom: 10,
                          background: ['pa_sold','sa_sold','ha_sold'].includes(lastDisposition.key) ? T.greenDim : T.goldDim,
                          border: `1px solid ${['pa_sold','sa_sold','ha_sold'].includes(lastDisposition.key) ? T.green : T.gold}40`,
                          display: 'flex', alignItems: 'center', gap: 10, fontSize: 14, fontWeight: 600,
                        }}
                      >
                        <span style={{ fontSize: 20 }}>{lastDisposition.icon}</span>
                        <span style={{ color: ['pa_sold','sa_sold','ha_sold'].includes(lastDisposition.key) ? T.green : T.gold }}>
                          {lastDisposition.label} — Moving to next lead...
                        </span>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {/* ─── FLASH CARD (Cornell Note Style) ─── */}
                  <AnimatePresence mode="wait">
                    <motion.div
                      key={currentLead.id}
                      initial={{ opacity: 0, x: 40 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -40 }}
                      transition={{ duration: 0.25, ease: 'easeOut' }}
                      style={{
                        background: T.card, borderRadius: 16, border: `1px solid ${T.border}`,
                        overflow: 'hidden',
                      }}
                    >
                      {/* Tier & Score Header Bar */}
                      <div style={{
                        padding: '10px 16px',
                        background: `linear-gradient(90deg, ${getTierColor(currentLead.tier)}15, transparent)`,
                        borderBottom: `1px solid ${T.border}`,
                        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                          <span style={{
                            padding: '2px 10px', borderRadius: 6,
                            background: `${getTierColor(currentLead.tier)}20`,
                            color: getTierColor(currentLead.tier),
                            fontSize: 12, fontWeight: 800, letterSpacing: 1, fontFamily: "'Cinzel', serif",
                          }}>
                            {currentLead.tier}-TIER
                          </span>
                          <span style={{
                            padding: '2px 8px', borderRadius: 4,
                            background: isAdSource(currentLead.source) ? `${T.cyan}20` : `${T.gold}20`,
                            color: isAdSource(currentLead.source) ? T.cyan : T.gold,
                            fontSize: 10, fontWeight: 700, letterSpacing: 0.5,
                          }}>
                            {isAdSource(currentLead.source) ? 'ADS' : 'SCRAPES'}
                          </span>
                          {/* Timezone calling indicator */}
                          {contactRules && (
                            <span style={{ fontSize: 14 }}>
                              {contactRules.callingStatus === 'green' ? '🟢' : contactRules.callingStatus === 'yellow' ? '🟡' : '🔴'}
                            </span>
                          )}
                        </div>
                        <ScoreRing score={currentLead.score} size={40} strokeWidth={3} />
                      </div>

                      {/* Cornell Layout */}
                      <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                          {/* LEFT: Lead Information */}
                          <div style={{ flex: '1 1 300px', padding: '16px', borderRight: `1px solid ${T.border}`, minWidth: 0 }}>
                            {/* Name (large) */}
                            <h2 style={{
                              fontFamily: "'Cinzel', serif", fontSize: 22, fontWeight: 700,
                              color: T.text, marginBottom: 4, lineHeight: 1.2,
                            }}>
                              {currentLead.first_name} {currentLead.last_name}
                            </h2>
                            {/* Phone tap-to-call */}
                            <a href={`tel:${currentLead.phone}`} style={{
                              fontSize: 16, color: T.gold, fontWeight: 600, textDecoration: 'none',
                              display: 'flex', alignItems: 'center', gap: 6, marginBottom: 12,
                            }}>
                              <Phone size={14} /> {formatPhone(currentLead.phone)}
                            </a>

                            {/* Reason / Intel */}
                            <div style={{
                              padding: '10px 12px', borderRadius: 10, background: T.surface,
                              border: `1px solid ${T.navy}30`, marginBottom: 12,
                            }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
                                <FileText size={13} color={T.gold} />
                                <span style={{ fontSize: 11, color: T.gold, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5 }}>Lead Intel</span>
                              </div>
                              <p style={{ fontSize: 13, color: T.text, lineHeight: 1.5 }}>{currentLead.reason || currentLead.situation}</p>
                              {currentLead.state && (
                                <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginTop: 6 }}>
                                  <MapPin size={11} color={T.textDim} />
                                  <span style={{ fontSize: 11, color: T.textDim }}>{currentLead.state} &bull; {getLocalTime(getLeadTimezone(currentLead))} local</span>
                                </div>
                              )}
                            </div>

                            {/* Score Breakdown */}
                            <div style={{
                              padding: '10px 12px', borderRadius: 10, background: T.surface,
                              border: `1px solid ${T.border}`, marginBottom: 12,
                            }}>
                              <span style={{ fontSize: 10, color: T.textMuted, textTransform: 'uppercase', letterSpacing: 0.5, display: 'block', marginBottom: 8 }}>Score Breakdown</span>
                              <ScoreBar label="Urgency" value={currentLead.urgency_score || 0} color={T.green} />
                              <ScoreBar label="Contactability" value={currentLead.contactability_score || 0} color={T.cyan} />
                              <ScoreBar label="Insurability" value={currentLead.insurability_score || 0} color={T.gold} />
                              <ScoreBar label="Monetization" value={currentLead.monetization_score || 0} color={T.green} />
                            </div>

                            {/* Contact Attempt Tracker */}
                            {contactRules && (
                              <div style={{
                                padding: '10px 12px', borderRadius: 10, background: T.surface,
                                border: `1px solid ${T.border}`, marginBottom: 12,
                              }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                                  <span style={{ fontSize: 11, color: T.textMuted, fontWeight: 600 }}>
                                    Attempt {contactRules.attempts} of {contactRules.maxAttempts}
                                  </span>
                                  <span style={{ fontSize: 10, color: T.textDim }}>
                                    Day {Math.min(contactRules.daysSinceCreated + 1, contactRules.maxDays)}/{contactRules.maxDays}
                                  </span>
                                </div>
                                <div style={{ width: '100%', height: 6, borderRadius: 3, background: T.bg }}>
                                  <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${(contactRules.attempts / contactRules.maxAttempts) * 100}%` }}
                                    transition={{ duration: 0.5 }}
                                    style={{
                                      height: '100%', borderRadius: 3,
                                      background: contactRules.attempts >= 18 ? T.orange
                                        : contactRules.attempts >= 10 ? T.gold : T.green,
                                    }}
                                  />
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 4 }}>
                                  <span style={{ fontSize: 10, color: T.textDim }}>Last: {timeAgo(contactRules.lastContacted)}</span>
                                  {contactRules.attempts >= 21 && (
                                    <span style={{ fontSize: 10, color: T.orange, fontWeight: 700 }}>MAX REACHED</span>
                                  )}
                                </div>
                              </div>
                            )}

                            {/* ─── ACTION BUTTONS ROW ─── */}
                            <a
                              href={`tel:${currentLead.phone}`}
                              style={{
                                display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
                                width: '100%', padding: '14px', borderRadius: 12, border: 'none',
                                background: contactRules?.canCall
                                  ? `linear-gradient(135deg, ${T.green}, #059669)`
                                  : `linear-gradient(135deg, ${T.orange}, #CC7000)`,
                                color: '#fff', fontSize: 16, fontWeight: 700, textDecoration: 'none',
                                fontFamily: "'Cinzel', serif", letterSpacing: 1,
                                boxShadow: contactRules?.canCall
                                  ? `0 4px 20px ${T.green}40`
                                  : `0 4px 20px ${T.orange}40`,
                                cursor: 'pointer', transition: 'all 0.2s',
                                animation: 'aegis-glow 3s ease-in-out infinite',
                              }}
                            >
                              <PhoneCall size={22} />
                              CALL {currentLead.first_name?.toUpperCase()}
                            </a>

                            {/* Secondary Actions */}
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 6, marginTop: 8 }}>
                              <button onClick={() => setShowTextComposer(true)} style={{
                                padding: '8px 4px', borderRadius: 8, border: `1px solid ${T.border}`,
                                background: T.surface, color: T.textMuted, cursor: 'pointer', fontSize: 10,
                                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3,
                              }}>
                                <MessageSquare size={14} /> Text
                              </button>
                              <button onClick={skipToBottom} style={{
                                padding: '8px 4px', borderRadius: 8, border: `1px solid ${T.border}`,
                                background: T.surface, color: T.textMuted, cursor: 'pointer', fontSize: 10,
                                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3,
                              }}>
                                <SkipForward size={14} /> Skip
                              </button>
                              <button onClick={sendToLauren} style={{
                                padding: '8px 4px', borderRadius: 8, border: `1px solid ${T.border}`,
                                background: T.surface, color: T.textMuted, cursor: 'pointer', fontSize: 10,
                                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3,
                              }}>
                                <UserPlus size={14} /> Lauren
                              </button>
                              <button onClick={() => navigator.clipboard?.writeText(currentLead.phone)} style={{
                                padding: '8px 4px', borderRadius: 8, border: `1px solid ${T.border}`,
                                background: T.surface, color: T.textMuted, cursor: 'pointer', fontSize: 10,
                                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3,
                              }}>
                                <Copy size={14} /> Copy #
                              </button>
                            </div>
                          </div>

                          {/* RIGHT: Notes Area */}
                          <div style={{ flex: '1 1 280px', padding: '16px', display: 'flex', flexDirection: 'column', minWidth: 0 }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 }}>
                              <FileText size={14} color={T.gold} />
                              <span style={{ fontSize: 13, fontWeight: 600, color: T.gold, fontFamily: "'Cinzel', serif" }}>NOTES</span>
                            </div>

                            <textarea
                              ref={noteRef}
                              value={noteText}
                              onChange={e => setNoteText(e.target.value)}
                              placeholder="Type notes about this call..."
                              onKeyDown={e => { if (e.key === 'Enter' && e.metaKey) saveNote(); }}
                              style={{
                                flex: 1, minHeight: 120, padding: '12px', borderRadius: 10,
                                background: T.surface, border: `1px solid ${T.border}`,
                                color: T.text, fontSize: 13, fontFamily: "'Inter', sans-serif",
                                resize: 'vertical', outline: 'none', lineHeight: 1.5,
                                transition: 'border-color 0.2s', boxSizing: 'border-box',
                              }}
                              onFocus={e => e.target.style.borderColor = T.navy}
                              onBlur={e => e.target.style.borderColor = T.border}
                            />

                            <div style={{ display: 'flex', gap: 6, marginTop: 8 }}>
                              <button onClick={saveNote} disabled={!noteText.trim()} style={{
                                flex: 1, padding: '10px', borderRadius: 8, border: 'none',
                                background: noteText.trim() ? T.navy : T.surface,
                                color: noteText.trim() ? T.text : T.textDim,
                                cursor: noteText.trim() ? 'pointer' : 'not-allowed',
                                fontSize: 12, fontWeight: 600, display: 'flex', alignItems: 'center',
                                justifyContent: 'center', gap: 6, transition: 'all 0.2s',
                              }}>
                                <Send size={12} /> Save Note
                              </button>
                              <span style={{ fontSize: 10, color: T.textDim, alignSelf: 'center' }}>Cmd+Enter</span>
                            </div>

                            {/* Existing DayDay Notes */}
                            {currentLead.dayday_notes && (
                              <div style={{
                                marginTop: 10, padding: '8px 10px', borderRadius: 8,
                                background: T.surface, border: `1px solid ${T.navy}30`,
                              }}>
                                <span style={{ fontSize: 10, color: T.navy, fontWeight: 600, display: 'block', marginBottom: 4 }}>SAVED NOTES</span>
                                <p style={{ fontSize: 12, color: T.text, lineHeight: 1.4, whiteSpace: 'pre-wrap' }}>{currentLead.dayday_notes}</p>
                              </div>
                            )}

                            {/* Note History */}
                            {currentLead.notes && currentLead.notes.length > 0 && (
                              <div style={{ marginTop: 12 }}>
                                <button onClick={() => setShowHistory(!showHistory)} style={{
                                  display: 'flex', alignItems: 'center', gap: 6, background: 'none',
                                  border: 'none', cursor: 'pointer', color: T.textMuted, fontSize: 12,
                                  fontWeight: 500, padding: 0, marginBottom: 6,
                                }}>
                                  {showHistory ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                                  History ({currentLead.notes.length})
                                </button>
                                <AnimatePresence>
                                  {showHistory && (
                                    <motion.div
                                      initial={{ height: 0, opacity: 0 }}
                                      animate={{ height: 'auto', opacity: 1 }}
                                      exit={{ height: 0, opacity: 0 }}
                                      style={{ overflow: 'hidden' }}
                                    >
                                      <div className="aegis-scroll" style={{
                                        maxHeight: 160, overflowY: 'auto',
                                        display: 'flex', flexDirection: 'column', gap: 6,
                                      }}>
                                        {[...currentLead.notes].reverse().map((note, i) => (
                                          <div key={i} style={{
                                            padding: '8px 10px', borderRadius: 8,
                                            background: T.surface, border: `1px solid ${T.border}`,
                                          }}>
                                            <p style={{ fontSize: 12, color: T.text, marginBottom: 4 }}>{note.text}</p>
                                            <div style={{ display: 'flex', gap: 8, fontSize: 10, color: T.textDim }}>
                                              <span>{note.by}</span>
                                              <span>{timeAgo(note.date)}</span>
                                            </div>
                                          </div>
                                        ))}
                                      </div>
                                    </motion.div>
                                  )}
                                </AnimatePresence>
                              </div>
                            )}
                          </div>
                        </div>

                        {/* ─── DISPOSITION BAR ─── */}
                        <div style={{
                          borderTop: `1px solid ${T.border}`, padding: '12px 16px',
                          background: T.surface,
                        }}>
                          <button onClick={() => setShowDispositions(!showDispositions)} style={{
                            width: '100%', padding: '10px', borderRadius: 10, border: `1px solid ${T.gold}30`,
                            background: T.goldDim, color: T.gold, cursor: 'pointer',
                            fontSize: 13, fontWeight: 700, fontFamily: "'Cinzel', serif",
                            letterSpacing: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
                            transition: 'all 0.2s',
                          }}>
                            <Target size={16} />
                            {showDispositions ? 'HIDE DISPOSITIONS' : 'DISPOSITION THIS LEAD'}
                            {showDispositions ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                          </button>

                          <AnimatePresence>
                            {showDispositions && (
                              <motion.div
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                style={{ overflow: 'hidden' }}
                              >
                                <div style={{
                                  display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))',
                                  gap: 8, marginTop: 10,
                                }}>
                                  {DISPOSITIONS.map(d => (
                                    <motion.button
                                      key={d.key}
                                      whileTap={{ scale: 0.95 }}
                                      onClick={() => handleDisposition(d)}
                                      style={{
                                        padding: '12px 10px', borderRadius: 10,
                                        border: `1px solid ${d.color}30`,
                                        background: `${d.color}10`,
                                        cursor: 'pointer', textAlign: 'center',
                                        transition: 'all 0.2s',
                                      }}
                                    >
                                      <span style={{ fontSize: 20, display: 'block', marginBottom: 4 }}>{d.icon}</span>
                                      <span style={{ fontSize: 12, fontWeight: 700, color: d.color, display: 'block' }}>{d.label}</span>
                                      <span style={{ fontSize: 10, color: T.textDim, display: 'block', marginTop: 2 }}>{d.desc}</span>
                                    </motion.button>
                                  ))}
                                </div>
                              </motion.div>
                            )}
                          </AnimatePresence>
                        </div>
                      </div>
                    </motion.div>
                  </AnimatePresence>

                  {/* ─── NEXT LEAD BUTTON ─── */}
                  <motion.button
                    whileTap={{ scale: 0.97 }}
                    onClick={goNext}
                    disabled={currentIndex >= leadsFiltered.length - 1}
                    style={{
                      width: '100%', padding: '14px', marginTop: 12, borderRadius: 12,
                      border: `1px solid ${T.navy}`,
                      background: `linear-gradient(135deg, ${T.navy}, ${T.navyDark})`,
                      color: T.gold, cursor: currentIndex >= leadsFiltered.length - 1 ? 'not-allowed' : 'pointer',
                      fontSize: 15, fontWeight: 700, fontFamily: "'Cinzel', serif",
                      letterSpacing: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
                      opacity: currentIndex >= leadsFiltered.length - 1 ? 0.4 : 1,
                      boxShadow: `0 4px 20px ${T.navy}30`,
                    }}
                  >
                    NEXT LEAD <ArrowRight size={18} />
                  </motion.button>

                  {/* Upcoming Callbacks */}
                  {stats.callbacks.length > 0 && (
                    <div style={{
                      marginTop: 16, padding: '14px', borderRadius: 12,
                      background: T.card, border: `1px solid ${T.border}`,
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 }}>
                        <Calendar size={14} color={T.gold} />
                        <span style={{ fontSize: 13, fontWeight: 600, color: T.gold, fontFamily: "'Cinzel', serif" }}>UPCOMING CALLBACKS</span>
                      </div>
                      {stats.callbacks.map((cb, i) => (
                        <div key={i} style={{
                          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                          padding: '8px 10px', borderRadius: 8, background: T.surface,
                          border: `1px solid ${T.border}`, marginBottom: i < stats.callbacks.length - 1 ? 6 : 0,
                        }}>
                          <div>
                            <p style={{ fontSize: 13, fontWeight: 600, color: T.text }}>{cb.name}</p>
                            <p style={{ fontSize: 11, color: T.textDim }}>{cb.date}</p>
                          </div>
                          <span style={{
                            padding: '4px 10px', borderRadius: 6,
                            background: T.goldDim, color: T.gold,
                            fontSize: 12, fontWeight: 600,
                          }}>
                            {cb.time}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : null}
            </motion.div>
          )}

          {/* ═══════════════════════════════════════════════ */}
          {/* ═══ PIPELINE TAB (CRM Table View) ═══ */}
          {/* ═══════════════════════════════════════════════ */}
          {mainTab === 'pipeline' && (
            <motion.div key="pipeline" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.2 }}>

              {/* Search */}
              <div style={{
                display: 'flex', alignItems: 'center', gap: 8,
                padding: '10px 12px', borderRadius: 10, background: T.surface,
                border: `1px solid ${T.border}`, marginBottom: 10,
              }}>
                <Search size={16} color={T.textDim} />
                <input
                  value={pipelineSearch}
                  onChange={e => setPipelineSearch(e.target.value)}
                  placeholder="Search leads..."
                  style={{
                    flex: 1, background: 'transparent', border: 'none', outline: 'none',
                    color: T.text, fontSize: 13, fontFamily: "'Inter', sans-serif",
                  }}
                />
                {pipelineSearch && (
                  <button onClick={() => setPipelineSearch('')} style={{
                    background: 'none', border: 'none', cursor: 'pointer', color: T.textDim,
                  }}>
                    <X size={14} />
                  </button>
                )}
              </div>

              {/* Filters */}
              <div style={{ display: 'flex', gap: 6, marginBottom: 10, flexWrap: 'wrap' }}>
                {/* Tier filter */}
                <select value={pipelineFilter.tier} onChange={e => setPipelineFilter(p => ({ ...p, tier: e.target.value }))} style={{
                  padding: '6px 10px', borderRadius: 6, border: `1px solid ${T.border}`,
                  background: T.surface, color: T.text, fontSize: 11, outline: 'none',
                  fontFamily: "'Inter', sans-serif",
                }}>
                  <option value="all">All Tiers</option>
                  <option value="A">A-Tier</option>
                  <option value="B">B-Tier</option>
                  <option value="C">C-Tier</option>
                </select>
                {/* Status filter */}
                <select value={pipelineFilter.status} onChange={e => setPipelineFilter(p => ({ ...p, status: e.target.value }))} style={{
                  padding: '6px 10px', borderRadius: 6, border: `1px solid ${T.border}`,
                  background: T.surface, color: T.text, fontSize: 11, outline: 'none',
                  fontFamily: "'Inter', sans-serif",
                }}>
                  <option value="all">All Status</option>
                  <option value="new">New</option>
                  <option value="contacted">Contacted</option>
                  <option value="callback">Callback</option>
                  <option value="sold">Sold</option>
                  <option value="disposed">Disposed</option>
                  <option value="no_answer">No Answer</option>
                  <option value="archived">Archived</option>
                </select>
                {/* Source filter */}
                <select value={pipelineFilter.source} onChange={e => setPipelineFilter(p => ({ ...p, source: e.target.value }))} style={{
                  padding: '6px 10px', borderRadius: 6, border: `1px solid ${T.border}`,
                  background: T.surface, color: T.text, fontSize: 11, outline: 'none',
                  fontFamily: "'Inter', sans-serif",
                }}>
                  <option value="all">All Sources</option>
                  <option value="ads">Ads</option>
                  <option value="scrapes">Scrapes</option>
                </select>
                {/* Assigned filter */}
                <select value={pipelineFilter.assigned} onChange={e => setPipelineFilter(p => ({ ...p, assigned: e.target.value }))} style={{
                  padding: '6px 10px', borderRadius: 6, border: `1px solid ${T.border}`,
                  background: T.surface, color: T.text, fontSize: 11, outline: 'none',
                  fontFamily: "'Inter', sans-serif",
                }}>
                  <option value="all">All Assigned</option>
                  <option value="DayDay">DayDay</option>
                  <option value="Lauren">Lauren</option>
                  <option value="unassigned">Unassigned</option>
                </select>
              </div>

              {/* Sort controls */}
              <div style={{ display: 'flex', gap: 6, marginBottom: 12 }}>
                <span style={{ fontSize: 11, color: T.textDim, alignSelf: 'center' }}>Sort:</span>
                {['score', 'name', 'date'].map(key => (
                  <button key={key} onClick={() => setPipelineSort(prev => ({
                    key, dir: prev.key === key ? (prev.dir === 'desc' ? 'asc' : 'desc') : 'desc'
                  }))} style={{
                    padding: '4px 10px', borderRadius: 6, border: `1px solid ${pipelineSort.key === key ? T.gold : T.border}`,
                    background: pipelineSort.key === key ? T.goldDim : T.surface,
                    color: pipelineSort.key === key ? T.gold : T.textMuted,
                    cursor: 'pointer', fontSize: 11, fontWeight: 600,
                    display: 'flex', alignItems: 'center', gap: 4,
                  }}>
                    {key.charAt(0).toUpperCase() + key.slice(1)}
                    {pipelineSort.key === key && (pipelineSort.dir === 'desc' ? <ArrowDown size={10} /> : <ArrowUp size={10} />)}
                  </button>
                ))}
                <span style={{ fontSize: 11, color: T.textDim, marginLeft: 'auto', alignSelf: 'center' }}>
                  {pipelineLeads.length} leads
                </span>
              </div>

              {/* Table */}
              <div className="aegis-scroll" style={{ overflowX: 'auto' }}>
                {/* Table Header */}
                <div style={{
                  display: 'grid', gridTemplateColumns: '1.5fr 1fr 0.5fr 0.5fr 0.8fr 0.8fr 0.6fr 0.6fr',
                  gap: 8, padding: '8px 12px', borderRadius: '10px 10px 0 0',
                  background: T.navyDark, minWidth: 700,
                }}>
                  {['Name', 'Phone', 'Score', 'Tier', 'Status', 'Source', 'Attempts', 'Assigned'].map(h => (
                    <span key={h} style={{ fontSize: 10, color: T.gold, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5 }}>{h}</span>
                  ))}
                </div>

                {/* Table Rows */}
                {pipelineLeads.length === 0 ? (
                  <div style={{ padding: '30px', textAlign: 'center', color: T.textDim, fontSize: 13 }}>
                    No leads match filters
                  </div>
                ) : pipelineLeads.map((lead, i) => (
                  <React.Fragment key={lead.id}>
                    <div
                      onClick={() => setExpandedRow(expandedRow === lead.id ? null : lead.id)}
                      style={{
                        display: 'grid', gridTemplateColumns: '1.5fr 1fr 0.5fr 0.5fr 0.8fr 0.8fr 0.6fr 0.6fr',
                        gap: 8, padding: '10px 12px', minWidth: 700,
                        background: i % 2 === 0 ? T.card : T.surface,
                        borderLeft: `3px solid ${getTierColor(lead.tier)}`,
                        cursor: 'pointer', transition: 'background 0.15s',
                      }}
                    >
                      <span style={{ fontSize: 13, fontWeight: 600, color: T.text, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {lead.first_name} {lead.last_name}
                      </span>
                      <span style={{ fontSize: 12, color: T.textMuted }}>{formatPhone(lead.phone)}</span>
                      <span style={{ fontSize: 13, fontWeight: 700, color: lead.score >= 80 ? T.green : lead.score >= 60 ? T.gold : T.orange }}>
                        {lead.score}
                      </span>
                      <span style={{
                        fontSize: 11, fontWeight: 800, color: getTierColor(lead.tier),
                      }}>{lead.tier}</span>
                      <span style={{
                        fontSize: 11, fontWeight: 600,
                        padding: '2px 8px', borderRadius: 4, alignSelf: 'center', textAlign: 'center',
                        background: lead.status === 'sold' ? T.greenDim
                          : lead.status === 'new' ? `${T.cyan}20`
                          : lead.status === 'callback' ? T.goldDim
                          : T.surface,
                        color: lead.status === 'sold' ? T.green
                          : lead.status === 'new' ? T.cyan
                          : lead.status === 'callback' ? T.gold
                          : T.textMuted,
                      }}>
                        {lead.status}
                      </span>
                      <span style={{
                        fontSize: 10, color: isAdSource(lead.source) ? T.cyan : T.gold,
                        fontWeight: 600,
                      }}>
                        {isAdSource(lead.source) ? 'ADS' : 'SCRAPE'}
                      </span>
                      <span style={{ fontSize: 12, color: T.textMuted }}>{lead.contact_attempts || 0}</span>
                      <span style={{ fontSize: 11, color: lead.assigned_to ? T.text : T.textDim }}>
                        {lead.assigned_to || '—'}
                      </span>
                    </div>

                    {/* Expanded Row Detail */}
                    <AnimatePresence>
                      {expandedRow === lead.id && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          style={{ overflow: 'hidden', minWidth: 700 }}
                        >
                          <div style={{
                            padding: '12px 16px', background: T.bg,
                            borderLeft: `3px solid ${getTierColor(lead.tier)}`,
                            borderBottom: `1px solid ${T.border}`,
                          }}>
                            <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
                              <div style={{ flex: '1 1 200px' }}>
                                <span style={{ fontSize: 10, color: T.textDim, display: 'block', marginBottom: 4 }}>SITUATION</span>
                                <p style={{ fontSize: 12, color: T.text, lineHeight: 1.4 }}>{lead.reason || lead.situation}</p>
                              </div>
                              <div style={{ flex: '0 0 140px' }}>
                                <span style={{ fontSize: 10, color: T.textDim, display: 'block', marginBottom: 4 }}>EMAIL</span>
                                <p style={{ fontSize: 12, color: T.text }}>{lead.email || '—'}</p>
                              </div>
                              <div style={{ flex: '0 0 80px' }}>
                                <span style={{ fontSize: 10, color: T.textDim, display: 'block', marginBottom: 4 }}>STATE</span>
                                <p style={{ fontSize: 12, color: T.text }}>{lead.state || lead.zip_code || '—'}</p>
                              </div>
                              <div style={{ flex: '0 0 100px' }}>
                                <span style={{ fontSize: 10, color: T.textDim, display: 'block', marginBottom: 4 }}>CREATED</span>
                                <p style={{ fontSize: 12, color: T.text }}>{timeAgo(lead.created_at)}</p>
                              </div>
                            </div>
                            {lead.dayday_notes && (
                              <div style={{ marginTop: 10 }}>
                                <span style={{ fontSize: 10, color: T.navy, fontWeight: 600 }}>DAYDAY NOTES:</span>
                                <p style={{ fontSize: 12, color: T.text, marginTop: 4, whiteSpace: 'pre-wrap' }}>{lead.dayday_notes}</p>
                              </div>
                            )}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </React.Fragment>
                ))}
              </div>
            </motion.div>
          )}

        </AnimatePresence>
      </div>

      {/* ─── CALLBACK MODAL ─── */}
      <AnimatePresence>
        {showCallbackModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowCallbackModal(false)}
            style={{
              position: 'fixed', inset: 0, zIndex: 100,
              background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(10px)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              padding: 20,
            }}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              onClick={e => e.stopPropagation()}
              style={{
                width: '100%', maxWidth: 380, borderRadius: 16,
                background: T.card, border: `1px solid ${T.border}`,
                padding: '24px', boxShadow: `0 20px 60px rgba(0,0,0,0.5)`,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
                <h3 style={{ fontFamily: "'Cinzel', serif", fontSize: 18, fontWeight: 700, color: T.gold }}>
                  Schedule Callback
                </h3>
                <button onClick={() => setShowCallbackModal(false)} style={{
                  background: 'none', border: 'none', cursor: 'pointer', color: T.textMuted,
                }}>
                  <X size={20} />
                </button>
              </div>

              {currentLead && (
                <p style={{ fontSize: 14, color: T.text, marginBottom: 16 }}>
                  For <strong>{currentLead.first_name} {currentLead.last_name}</strong>
                </p>
              )}

              <div style={{ marginBottom: 12 }}>
                <label style={{ fontSize: 12, color: T.textMuted, display: 'block', marginBottom: 4 }}>Date</label>
                <input
                  type="date"
                  value={callbackDate}
                  onChange={e => setCallbackDate(e.target.value)}
                  style={{
                    width: '100%', padding: '10px 12px', borderRadius: 8,
                    background: T.surface, border: `1px solid ${T.border}`,
                    color: T.text, fontSize: 14, outline: 'none',
                    fontFamily: "'Inter', sans-serif", boxSizing: 'border-box',
                  }}
                />
              </div>

              <div style={{ marginBottom: 20 }}>
                <label style={{ fontSize: 12, color: T.textMuted, display: 'block', marginBottom: 4 }}>Time</label>
                <input
                  type="time"
                  value={callbackTime}
                  onChange={e => setCallbackTime(e.target.value)}
                  style={{
                    width: '100%', padding: '10px 12px', borderRadius: 8,
                    background: T.surface, border: `1px solid ${T.border}`,
                    color: T.text, fontSize: 14, outline: 'none',
                    fontFamily: "'Inter', sans-serif", boxSizing: 'border-box',
                  }}
                />
              </div>

              <button
                onClick={handleCallbackSchedule}
                disabled={!callbackDate || !callbackTime}
                style={{
                  width: '100%', padding: '12px', borderRadius: 10, border: 'none',
                  background: callbackDate && callbackTime ? `linear-gradient(135deg, ${T.gold}, #B8941F)` : T.surface,
                  color: callbackDate && callbackTime ? T.bg : T.textDim,
                  cursor: callbackDate && callbackTime ? 'pointer' : 'not-allowed',
                  fontSize: 14, fontWeight: 700, fontFamily: "'Cinzel', serif",
                  letterSpacing: 1,
                }}
              >
                <Calendar size={16} style={{ display: 'inline', marginRight: 8, verticalAlign: 'middle' }} />
                SCHEDULE CALLBACK
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ─── TEXT COMPOSER OVERLAY ─── */}
      <AnimatePresence>
        {showTextComposer && currentLead && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowTextComposer(false)}
            style={{
              position: 'fixed', inset: 0, zIndex: 100,
              background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(10px)',
              display: 'flex', alignItems: 'flex-end', justifyContent: 'center',
              padding: '0 12px 20px',
            }}
          >
            <motion.div
              initial={{ y: 100, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: 100, opacity: 0 }}
              onClick={e => e.stopPropagation()}
              style={{
                width: '100%', maxWidth: 420, borderRadius: 16,
                background: T.card, border: `1px solid ${T.gold}30`,
                overflow: 'hidden', boxShadow: `0 -10px 40px rgba(0,0,0,0.5)`,
              }}
            >
              <div style={{
                padding: '12px 16px', background: T.goldDim,
                borderBottom: `1px solid ${T.gold}20`,
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <MessageSquare size={16} color={T.gold} />
                  <span style={{ fontSize: 13, fontWeight: 700, color: T.gold, fontFamily: "'Cinzel', serif" }}>
                    TEXT {currentLead.first_name?.toUpperCase()}
                  </span>
                </div>
                <button onClick={() => setShowTextComposer(false)} style={{
                  background: 'none', border: 'none', cursor: 'pointer', color: T.textMuted,
                }}>
                  <X size={18} />
                </button>
              </div>

              <div style={{ padding: '12px 16px' }}>
                {/* Template selector */}
                <div style={{ display: 'flex', gap: 6, marginBottom: 10 }}>
                  {TEXT_TEMPLATES.map((tmpl, i) => (
                    <button key={i} onClick={() => { setSelectedTemplate(i); setTemplateText(tmpl.text); }} style={{
                      flex: 1, padding: '6px 4px', borderRadius: 6,
                      border: `1px solid ${selectedTemplate === i ? T.gold : T.border}`,
                      background: selectedTemplate === i ? T.goldDim : T.surface,
                      color: selectedTemplate === i ? T.gold : T.textMuted,
                      cursor: 'pointer', fontSize: 10, fontWeight: 600,
                    }}>
                      {tmpl.label}
                    </button>
                  ))}
                </div>

                <textarea
                  value={templateText}
                  onChange={e => setTemplateText(e.target.value)}
                  style={{
                    width: '100%', minHeight: 100, padding: '10px 12px', borderRadius: 8,
                    background: T.surface, border: `1px solid ${T.border}`,
                    color: T.text, fontSize: 13, fontFamily: "'Inter', sans-serif",
                    resize: 'none', outline: 'none', lineHeight: 1.5, boxSizing: 'border-box',
                  }}
                />

                <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
                  <button onClick={() => {
                    navigator.clipboard?.writeText(templateText);
                    setCopiedText(true);
                    setTimeout(() => setCopiedText(false), 2000);
                  }} style={{
                    flex: 1, padding: '10px', borderRadius: 8, border: 'none',
                    background: copiedText ? T.greenDim : T.navy,
                    color: copiedText ? T.green : T.gold,
                    cursor: 'pointer', fontSize: 13, fontWeight: 700,
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
                    fontFamily: "'Cinzel', serif",
                  }}>
                    {copiedText ? <><CheckCircle2 size={14} /> COPIED</> : <><Copy size={14} /> COPY TO CLIPBOARD</>}
                  </button>
                </div>

                <a href={`sms:${currentLead.phone}&body=${encodeURIComponent(templateText)}`} style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
                  width: '100%', padding: '10px', marginTop: 8, borderRadius: 8,
                  background: T.greenDim, border: `1px solid ${T.green}30`,
                  color: T.green, textDecoration: 'none', fontSize: 13, fontWeight: 700,
                  fontFamily: "'Cinzel', serif",
                }}>
                  <Send size={14} /> OPEN IN MESSAGES
                </a>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ─── AEGIS COMPOSER (Floating Panel) ─── */}
      <AnimatePresence>
        {showComposer && (
          <motion.div
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 100 }}
            style={{
              position: 'fixed', bottom: 80, left: 12, right: 12, zIndex: 90,
              maxWidth: 500, margin: '0 auto',
              borderRadius: 16, background: T.card,
              border: `1px solid ${T.gold}30`,
              boxShadow: `0 -10px 40px rgba(0,0,0,0.5), 0 0 30px ${T.gold}10`,
              overflow: 'hidden',
            }}
          >
            <div style={{
              padding: '12px 16px', background: T.goldDim,
              borderBottom: `1px solid ${T.gold}20`,
              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <Bot size={16} color={T.gold} />
                <span style={{ fontSize: 13, fontWeight: 700, color: T.gold, fontFamily: "'Cinzel', serif" }}>
                  AEGIS COMPOSER
                </span>
              </div>
              <button onClick={() => setShowComposer(false)} style={{
                background: 'none', border: 'none', cursor: 'pointer', color: T.textMuted,
              }}>
                <X size={18} />
              </button>
            </div>

            <div style={{ padding: '16px' }}>
              <p style={{ fontSize: 11, color: T.textDim, marginBottom: 8 }}>
                Type your rough text. AEGIS will rewrite it professionally.
              </p>

              <textarea
                value={composerInput}
                onChange={e => setComposerInput(e.target.value)}
                placeholder="e.g., hey i saw u need health insurance, i can help u out..."
                style={{
                  width: '100%', minHeight: 70, padding: '10px 12px', borderRadius: 8,
                  background: T.surface, border: `1px solid ${T.border}`,
                  color: T.text, fontSize: 13, fontFamily: "'Inter', sans-serif",
                  resize: 'none', outline: 'none', lineHeight: 1.4,
                  boxSizing: 'border-box',
                }}
              />

              <button
                onClick={handleComposerRewrite}
                disabled={!composerInput.trim()}
                style={{
                  width: '100%', padding: '10px', marginTop: 8, borderRadius: 8, border: 'none',
                  background: composerInput.trim() ? `linear-gradient(135deg, ${T.navy}, ${T.navyLight})` : T.surface,
                  color: composerInput.trim() ? T.gold : T.textDim,
                  cursor: composerInput.trim() ? 'pointer' : 'not-allowed',
                  fontSize: 13, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6,
                }}
              >
                <Sparkles size={14} /> REWRITE WITH AEGIS
              </button>

              {composerOutput && (
                <div style={{
                  marginTop: 12, padding: '12px', borderRadius: 8,
                  background: T.greenDim, border: `1px solid ${T.green}30`,
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
                    <span style={{ fontSize: 11, color: T.green, fontWeight: 600 }}>AEGIS REWRITE</span>
                    <button onClick={() => {
                      navigator.clipboard?.writeText(composerOutput);
                    }} style={{
                      padding: '3px 8px', borderRadius: 4, border: `1px solid ${T.green}30`,
                      background: 'transparent', color: T.green, cursor: 'pointer',
                      fontSize: 10, fontWeight: 600, display: 'flex', alignItems: 'center', gap: 4,
                    }}>
                      <Copy size={10} /> Copy
                    </button>
                  </div>
                  <p style={{ fontSize: 13, color: T.text, lineHeight: 1.5 }}>{composerOutput}</p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ─── FLOATING COMPOSER BUTTON ─── */}
      <motion.button
        whileTap={{ scale: 0.9 }}
        onClick={() => setShowComposer(!showComposer)}
        style={{
          position: 'fixed', bottom: 20, right: 20, zIndex: 80,
          width: 56, height: 56, borderRadius: '50%',
          background: `linear-gradient(135deg, ${T.navy}, ${T.navyLight})`,
          border: `2px solid ${T.gold}40`,
          boxShadow: `0 4px 20px ${T.navy}60`,
          cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
          animation: 'aegis-float 3s ease-in-out infinite',
        }}
      >
        {showComposer ? <X size={22} color={T.gold} /> : <Bot size={22} color={T.gold} />}
      </motion.button>

      {/* ─── BOTTOM NAV (Spacing) ─── */}
      <div style={{ height: 80 }} />
    </div>
  );
}
