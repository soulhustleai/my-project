// Vercel Serverless Function — AEGIS Lead Intake Submission
// Handles form POST, inserts to Supabase with service key (server-side, secure)

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const SUPABASE_URL = 'https://pjkurxtvvtxbpfearqhd.supabase.co';
  const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;

  try {
    const lead = req.body;

    // Insert lead
    const response = await fetch(`${SUPABASE_URL}/rest/v1/aegis_leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify(lead)
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Supabase error:', err);
      return res.status(500).json({ error: 'Failed to save lead' });
    }

    return res.status(201).json({ success: true });
  } catch (e) {
    console.error('Submit error:', e);
    return res.status(500).json({ error: 'Server error' });
  }
}
