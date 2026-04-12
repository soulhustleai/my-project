-- APEX cover sync — products.cover_url
-- Run once the Apex cover branch is pushed to main (or keep pointing at the
-- claude/setup-apex-2pYgf branch while it's still a WIP branch).
--
-- To run manually:
--   psql $SUPABASE_URL -f update_product_covers.sql
-- Or via the MCP:
--   mcp__supabase__execute_sql with project_id=pjkurxtvvtxbpfearqhd
--
-- Idempotent: safe to re-run. Matches on slug.

WITH cover_map(slug, cover_file) AS (
  VALUES
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
WHERE  p.slug = cm.slug
RETURNING p.slug, p.name, p.cover_url;

-- After the branch is merged to main, rerun with the main-branch URL:
--
-- WITH cover_map(slug, cover_file) AS ( ... same list ... )
-- UPDATE public.products p
-- SET cover_url = 'https://raw.githubusercontent.com/soulhustleai/my-project/main/god-mode-credit/assets/apex/covers/' || cm.cover_file,
--     updated_at = NOW()
-- FROM cover_map cm WHERE p.slug = cm.slug;
