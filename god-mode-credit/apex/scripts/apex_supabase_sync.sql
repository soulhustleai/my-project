-- =============================================================================
-- APEX — Consolidated Supabase Sync
-- =============================================================================
-- Idempotent single-file sync for everything Apex touches in the soulhustleai
-- Supabase project (pjkurxtvvtxbpfearqhd). Safe to re-run.
--
--   1. DDL: ceo_brains.avatar_url column (if missing)
--   2. ceo_brains: set APEX voice_id + avatar_url + business
--   3. sovereign_vault: upsert apex_avatar_url + variants as config keys
--   4. products: sync cover_url for all 11 GMC products
--
-- To run:
--   mcp__supabase__execute_sql  project_id=pjkurxtvvtxbpfearqhd
--                                query="$(cat apex_supabase_sync.sql)"
--   -- or --
--   psql "$DATABASE_URL" -f apex_supabase_sync.sql
--
-- =============================================================================

BEGIN;

-- -------------------------------------------------------------------------
-- 1. Schema: add avatar_url to ceo_brains if missing
-- -------------------------------------------------------------------------
ALTER TABLE public.ceo_brains
  ADD COLUMN IF NOT EXISTS avatar_url TEXT;

COMMENT ON COLUMN public.ceo_brains.avatar_url IS
  'Canonical character portrait URL for the CEO persona. Used as PFP, email avatar, system UI avatar, and Vapi assistant image.';

-- -------------------------------------------------------------------------
-- 2. ceo_brains: lock APEX voice + avatar + business
-- -------------------------------------------------------------------------
UPDATE public.ceo_brains
SET
  voice_id   = 'ErXwobaYiN019PkySvjV',  -- ElevenLabs Antoni (from sovereign_vault.elevenlabs_api_key)
  business   = COALESCE(NULLIF(business, ''), 'GOD MODE CREDIT'),
  avatar_url = 'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar.png',
  updated_at = NOW()
WHERE UPPER(name) = 'APEX';

-- -------------------------------------------------------------------------
-- 3. sovereign_vault: upsert apex avatar variants as config keys
-- -------------------------------------------------------------------------
-- Uses INSERT .. ON CONFLICT (key_name) DO UPDATE so reruns just refresh.
-- NOTE: if sovereign_vault does not have a unique constraint on key_name,
-- the ON CONFLICT will no-op. In that case the WHERE NOT EXISTS fallback
-- below keeps it idempotent.

INSERT INTO public.sovereign_vault
  (key_name, key_value, key_type, service, description, environment, is_active, created_at, updated_at)
SELECT * FROM (VALUES
  ('apex_avatar_url',
   'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar.png',
   'url', 'GOD MODE CREDIT',
   'Canonical APEX portrait (full throne seated, 848x1264 PNG). Use this URL for emails, VSL overlays, Vapi assistant image, product page author photo.',
   'production', true, NOW(), NOW()),
  ('apex_avatar_square_url',
   'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar-square.png',
   'url', 'GOD MODE CREDIT',
   'APEX square PFP crop (848x848 PNG). Use for TikTok/IG/YouTube profile pictures, Discord avatar, Twitter profile.',
   'production', true, NOW(), NOW()),
  ('apex_avatar_face_url',
   'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar-face-512.png',
   'url', 'GOD MODE CREDIT',
   'APEX tight face crop (512x512 PNG). Use for small UI avatars (ManyChat, ConvertKit, dashboard widgets).',
   'production', true, NOW(), NOW()),
  ('apex_avatar_web_url',
   'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar-web.png',
   'url', 'GOD MODE CREDIT',
   'APEX web-optimized portrait (680x1014 PNG). Use for website hero sections, Stan Store bio link hero, email headers.',
   'production', true, NOW(), NOW())
) AS v(key_name, key_value, key_type, service, description, environment, is_active, created_at, updated_at)
WHERE NOT EXISTS (
  SELECT 1 FROM public.sovereign_vault sv WHERE sv.key_name = v.key_name
);

-- Re-sync values for existing rows (handles reruns after URL changes)
UPDATE public.sovereign_vault
SET key_value = 'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar.png',
    updated_at = NOW()
WHERE key_name = 'apex_avatar_url';

UPDATE public.sovereign_vault
SET key_value = 'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar-square.png',
    updated_at = NOW()
WHERE key_name = 'apex_avatar_square_url';

UPDATE public.sovereign_vault
SET key_value = 'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar-face-512.png',
    updated_at = NOW()
WHERE key_name = 'apex_avatar_face_url';

UPDATE public.sovereign_vault
SET key_value = 'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/apex/avatar-web.png',
    updated_at = NOW()
WHERE key_name = 'apex_avatar_web_url';

-- -------------------------------------------------------------------------
-- 4. products: sync cover_url for all 11 GMC products
-- -------------------------------------------------------------------------
WITH cover_map(slug, cover_file) AS (VALUES
  ('5-federal-laws',            '01-5-federal-laws.png'),
  ('cards-that-say-yes',        '02-cards-that-say-yes.png'),
  ('ai-x-credit-cheat-code',    '03-ai-x-credit-cheat-code.png'),
  ('ai-credit-repair-toolkit',  '04-ai-credit-repair-toolkit.png'),
  ('the-dispute-letter-pack',   '05-the-dispute-letter-pack.png'),
  ('zero-to-10k-ai-playbook',   '06-zero-to-10k-ai-automation-playbook.png'),
  ('collect-what-they-owe-you', '07-collect-what-they-owe-you.png'),
  ('business-credit-blueprint', '08-business-credit-blueprint.png'),
  ('zero-to-funded-bundle',     '09-zero-to-funded-bundle.png'),
  ('credit-ascension',          '10-credit-ascension.png'),
  ('the-crowned-circle',        '11-the-crowned-circle.png')
)
UPDATE public.products p
SET    cover_url  = 'https://raw.githubusercontent.com/soulhustleai/my-project/claude/setup-apex-2pYgf/god-mode-credit/assets/apex/covers/' || cm.cover_file,
       updated_at = NOW()
FROM   cover_map cm
WHERE  p.slug = cm.slug;

COMMIT;

-- -------------------------------------------------------------------------
-- 5. Verification (read-only, safe to paste into a new session)
-- -------------------------------------------------------------------------
-- SELECT name, voice_id, avatar_url FROM ceo_brains WHERE UPPER(name)='APEX';
-- SELECT key_name, key_value FROM sovereign_vault WHERE key_name LIKE 'apex_avatar%';
-- SELECT slug, cover_url FROM products WHERE cover_url LIKE '%apex%' ORDER BY slug;
