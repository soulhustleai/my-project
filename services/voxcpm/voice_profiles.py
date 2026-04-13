"""
Godfident Empire — Per-CEO Voice Psychoacoustic Profiles

Every CEO has a locked voice profile that gets applied to their TTS render
as a post-processing filter chain. The profile encodes:

  - Target fundamental frequency range (F0) for the underlying TTS pick
  - Target speaking rate (WPM) for script design
  - EQ curve — high-pass, proximity boost, mid-cut, presence, airband
  - Compression — ratio, threshold, attack, release
  - Reverb — pre-delay, decay, wet level
  - Loudness — target LUFS (EBU R128 / Apple Podcast standard)
  - Sonic logo — which stinger to append as the tail

Grounded in peer-reviewed psychoacoustics research — see
docs/VOICE-PSYCHOACOUSTICS.md for full citations.

The profiles are chosen to match each CEO's personality AND to maximize
emotional recall + return engagement via:
  - Low-mid proximity boost (200-500 Hz) → intimacy / "speaking in your ear"
  - 2-5 kHz presence boost → clarity / cut-through on phone speakers
  - LUFS normalization → consistent loudness across every CEO asset
  - Sonic logo tail → conditioned "feel good" cue via mere-exposure effect

Every profile ends with a 500ms crossfade into the CEO's 528/741/963 Hz
solfeggio-anchored sonic logo (see services/voxcpm/sonic_branding.py).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EQBand:
    """A single parametric EQ band."""
    filter_type: str   # "highpass" | "lowpass" | "peak" | "lowshelf" | "highshelf"
    freq_hz: float
    gain_db: float = 0.0
    q: float = 1.0


@dataclass
class Compression:
    ratio: float           # compression ratio (e.g. 3.0 = 3:1)
    threshold_db: float    # dB threshold (e.g. -16.0)
    attack_ms: float
    release_ms: float
    makeup_gain_db: float = 0.0


@dataclass
class Reverb:
    predelay_ms: int       # time before reverb starts (creates "space")
    decay_s: float         # total reverb tail length
    wet_db: float          # wet level in dB below dry signal


@dataclass
class VoiceProfile:
    ceo: str                       # "APEX"
    f0_range_hz: tuple[int, int]   # e.g. (100, 160) — target pitch range for TTS pick
    wpm_target: int                # target words per minute
    eq_bands: list[EQBand] = field(default_factory=list)
    compression: Optional[Compression] = None
    reverb: Optional[Reverb] = None
    lufs_target: float = -16.0     # integrated LUFS target
    true_peak_db: float = -1.5     # true peak ceiling
    sonic_logo: str = ""           # filename stem in voice-samples/sonic-logos/
    mood_tag: str = ""             # human-readable mood
    notes: str = ""                # design rationale


# ============================================================================
# THE 12 CEO PROFILES
# ============================================================================
# Common EQ pattern:
#   highpass 70-100 Hz   → clean subsonic rumble
#   peak 200-300 Hz      → proximity boost for intimacy (boost)
#   peak 400-800 Hz      → mid-cut (un-muddy, un-honk) (cut)
#   peak 2.5-4.5 kHz     → presence boost for clarity
#   peak 10-13 kHz       → airband for "silk" and warmth
#
# WPM targets based on UCLA Communication 2015 + NCVS research:
#   130-140 slow authoritative, trust-first
#   150-160 optimal comprehension + business competence
#   160-170 high-energy, entertaining, counter-attitudinal persuasion
#   170+    hungry/urgent
# ============================================================================

PROFILES: dict[str, VoiceProfile] = {

    "APEX": VoiceProfile(
        ceo="APEX",
        f0_range_hz=(100, 160),
        wpm_target=150,
        eq_bands=[
            EQBand("highpass", 80,   0,   0.707),
            EQBand("peak",     250,  2.0, 1.0),    # proximity boost: intimate close-mic feel
            EQBand("peak",     450, -2.0, 1.2),    # un-muddy
            EQBand("peak",     3500, 2.0, 1.0),    # presence: clarity on phones
            EQBand("peak",     12000, 1.0, 0.8),   # airband: warmth
        ],
        compression=Compression(ratio=3.0, threshold_db=-16.0, attack_ms=15, release_ms=80),
        reverb=Reverb(predelay_ms=40, decay_s=0.3, wet_db=-18),
        lufs_target=-16.0,
        sonic_logo="apex-credit-ascension",
        mood_tag="young teacher, calm kitchen-table cousin",
        notes="Matches Miles voice — young NY Black Gen Z teacher. Pro-attitudinal content "
              "(listeners already suspect the system is rigged), so slower = more trust (150 WPM).",
    ),

    "ZERO": VoiceProfile(
        ceo="ZERO",
        f0_range_hz=(95, 150),
        wpm_target=165,
        eq_bands=[
            EQBand("highpass", 80,   0,   0.707),
            EQBand("peak",     300,  3.0, 1.0),    # thicker proximity for NY street warmth
            EQBand("peak",     550, -1.5, 1.3),    # de-honk
            EQBand("peak",     4000, 3.0, 1.0),    # strong presence — social-feed cut-through
            EQBand("peak",     13000, 2.0, 0.8),   # bright airband for energy
        ],
        compression=Compression(ratio=4.0, threshold_db=-18.0, attack_ms=10, release_ms=100),
        reverb=Reverb(predelay_ms=60, decay_s=0.8, wet_db=-14),
        lufs_target=-14.0,  # social-loud for TikTok/Reels
        sonic_logo="zero-soulhustleai",
        mood_tag="NY urban hype-man, smooth sultry",
        notes="Matches Tyrese Tate. Entertaining register → higher WPM (165). Louder LUFS target "
              "(-14) so he cuts through the feed above Apex's -16.",
    ),

    "SOVEREIGN": VoiceProfile(
        ceo="SOVEREIGN",
        f0_range_hz=(85, 140),
        wpm_target=135,
        eq_bands=[
            EQBand("highpass", 70,   0,   0.707),
            EQBand("peak",     200,  3.0, 1.0),    # deep proximity — gravitas authority
            EQBand("peak",     1000, -1.0, 1.5),   # avoid nasal center
            EQBand("peak",     3000, 1.5, 1.0),    # subtle presence (authority not hype)
            EQBand("peak",     11000, 1.0, 0.8),
        ],
        compression=Compression(ratio=3.0, threshold_db=-14.0, attack_ms=20, release_ms=120),
        reverb=Reverb(predelay_ms=80, decay_s=1.2, wet_db=-16),  # majestic hall
        lufs_target=-16.0,
        sonic_logo="sovereign-godfident",
        mood_tag="the parent, highest authority, Edwin's digital super-self",
        notes="Slow (135 WPM) for maximum trust + authority. Lowest F0 range in the roster — "
              "research shows lower F0 = more trusted (Baus 2017 PLOS ONE). Long hall reverb for "
              "majesty without washing out intelligibility.",
    ),

    "MIDAS": VoiceProfile(
        ceo="MIDAS",
        f0_range_hz=(90, 150),
        wpm_target=155,
        eq_bands=[
            EQBand("highpass", 80,   0,   0.707),
            EQBand("peak",     250,  2.5, 1.0),
            EQBand("peak",     500, -1.5, 1.2),
            EQBand("peak",     3800, 2.5, 1.0),
            EQBand("peak",     12000, 1.0, 0.8),
        ],
        compression=Compression(ratio=3.5, threshold_db=-16.0, attack_ms=12, release_ms=90),
        reverb=Reverb(predelay_ms=50, decay_s=0.6, wet_db=-17),
        lufs_target=-15.0,
        sonic_logo="midas-recovery",
        mood_tag="smooth closer with legal precision",
        notes="Mid-tempo for business scenarios (UCLA 2015 found fast speakers rated 30% more competent "
              "in business contexts). Warm proximity so the 'we're on the same side of the table' "
              "feeling comes through.",
    ),

    "AEGIS": VoiceProfile(
        ceo="AEGIS",
        f0_range_hz=(95, 155),
        wpm_target=145,
        eq_bands=[
            EQBand("highpass", 75,   0,   0.707),
            EQBand("peak",     250,  3.0, 1.0),    # max warmth — big brother energy
            EQBand("peak",     550, -1.5, 1.2),
            EQBand("peak",     3500, 2.0, 1.0),
            EQBand("peak",     12000, 1.0, 0.8),
        ],
        compression=Compression(ratio=3.0, threshold_db=-15.0, attack_ms=18, release_ms=100),
        reverb=Reverb(predelay_ms=60, decay_s=0.5, wet_db=-19),  # close room
        lufs_target=-16.0,
        sonic_logo="aegis-shield",
        mood_tag="warm protective big brother, health context",
        notes="Slowest of the SoulHustleAI stack (145 WPM). Health-topic content requires trust > "
              "excitement. Closer room reverb → intimate one-on-one advisor feel.",
    ),

    "CERBERUS": VoiceProfile(
        ceo="CERBERUS",
        f0_range_hz=(80, 130),
        wpm_target=130,
        eq_bands=[
            EQBand("highpass", 65,   0,   0.707),  # preserve sub bass
            EQBand("peak",     180,  4.0, 0.9),    # biggest bass lift — guardian weight
            EQBand("peak",     500, -2.0, 1.2),
            EQBand("peak",     2800, 1.5, 1.0),
            EQBand("peak",     10000, -1.0, 0.8),  # slightly darken airband — harder, less friendly
        ],
        compression=Compression(ratio=4.0, threshold_db=-14.0, attack_ms=8, release_ms=120),
        reverb=Reverb(predelay_ms=100, decay_s=1.4, wet_db=-15),  # cavernous
        lufs_target=-15.0,
        sonic_logo="cerberus-guardian",
        mood_tag="three-headed guardian, gruff protective",
        notes="Lowest F0, slowest WPM (130). Big bass proximity + long reverb tail creates a 'you're "
              "safe under this guardian' psychoacoustic envelope. Darker airband (cut at 10kHz) "
              "reduces 'friendly' sparkle and increases seriousness.",
    ),

    "CLOSER": VoiceProfile(
        ceo="CLOSER",
        f0_range_hz=(95, 155),
        wpm_target=170,
        eq_bands=[
            EQBand("highpass", 80,   0,   0.707),
            EQBand("peak",     280,  2.5, 1.0),
            EQBand("peak",     500, -1.0, 1.3),
            EQBand("peak",     4000, 3.0, 1.0),
            EQBand("peak",     13000, 2.0, 0.8),
        ],
        compression=Compression(ratio=5.0, threshold_db=-18.0, attack_ms=6, release_ms=60),  # tight
        reverb=Reverb(predelay_ms=30, decay_s=0.4, wet_db=-18),  # focused, up-front
        lufs_target=-14.0,
        sonic_logo="closer-sales",
        mood_tag="fast aggressive smooth closer, chess-player",
        notes="Fastest of the business CEOs. UCLA 2015 — fast speakers 25% more persuasive in sales "
              "contexts, especially counter-attitudinal (new clients who aren't sure yet). Tight "
              "compression (5:1) + short reverb = up-in-your-face urgency without chaos.",
    ),

    "HUNTER": VoiceProfile(
        ceo="HUNTER",
        f0_range_hz=(100, 165),
        wpm_target=175,
        eq_bands=[
            EQBand("highpass", 85,   0,   0.707),
            EQBand("peak",     260,  2.0, 1.0),
            EQBand("peak",     4200, 3.0, 1.0),
            EQBand("peak",     13000, 2.0, 0.8),
        ],
        compression=Compression(ratio=5.0, threshold_db=-18.0, attack_ms=5, release_ms=50),
        reverb=Reverb(predelay_ms=25, decay_s=0.3, wet_db=-20),  # dry, urgent
        lufs_target=-14.0,
        sonic_logo="hunter-leads",
        mood_tag="driven predator, hungry",
        notes="Fastest in the roster (175 WPM). Very dry signal (-20dB wet) → urgency, no time "
              "for pretty reverb. Highest attack compression → every word punches.",
    ),

    "KEEPER": VoiceProfile(
        ceo="KEEPER",
        f0_range_hz=(95, 150),
        wpm_target=140,
        eq_bands=[
            EQBand("highpass", 75,   0,   0.707),
            EQBand("peak",     240,  2.5, 1.0),
            EQBand("peak",     3200, 1.5, 1.0),
            EQBand("peak",     12000, 1.5, 0.8),
        ],
        compression=Compression(ratio=2.5, threshold_db=-15.0, attack_ms=20, release_ms=150),  # open
        reverb=Reverb(predelay_ms=70, decay_s=0.7, wet_db=-17),  # soft embrace
        lufs_target=-16.0,
        sonic_logo="keeper-retention",
        mood_tag="calm nurturing librarian, perceptive",
        notes="Slow WPM + open compression = natural uncompressed feel. Keeper is the CEO who "
              "LISTENS more than talks — his audio should feel like breathing room.",
    ),

    "BUILDER": VoiceProfile(
        ceo="BUILDER",
        f0_range_hz=(100, 155),
        wpm_target=150,
        eq_bands=[
            EQBand("highpass", 80,   0,   0.707),
            EQBand("peak",     230,  2.0, 1.0),
            EQBand("peak",     800, -1.0, 1.3),    # de-congest technical mid-range
            EQBand("peak",     3500, 2.0, 1.0),
            EQBand("peak",     12000, 1.5, 0.8),
        ],
        compression=Compression(ratio=3.0, threshold_db=-16.0, attack_ms=15, release_ms=80),
        reverb=Reverb(predelay_ms=50, decay_s=0.5, wet_db=-18),
        lufs_target=-16.0,
        sonic_logo="builder-systems",
        mood_tag="calm technical architect",
        notes="Mid-tempo informative content. De-congesting mid-cut at 800 Hz keeps technical "
              "explanations clear even when the script is dense.",
    ),

    "VEGA": VoiceProfile(
        ceo="VEGA",
        f0_range_hz=(180, 280),   # female range
        wpm_target=150,
        eq_bands=[
            EQBand("highpass", 100,  0,   0.707),  # tighter HP for female voice
            EQBand("peak",     400,  2.0, 1.0),    # proximity boost higher for female F0
            EQBand("peak",     1200, -1.0, 1.4),   # avoid honk / boxiness
            EQBand("peak",     4000, 2.0, 1.0),
            EQBand("peak",     12500, 2.0, 0.8),
        ],
        compression=Compression(ratio=3.0, threshold_db=-16.0, attack_ms=15, release_ms=90),
        reverb=Reverb(predelay_ms=70, decay_s=0.8, wet_db=-16),
        lufs_target=-16.0,
        sonic_logo="vega-operations",
        mood_tag="authoritative command-layer female general",
        notes="Female voice requires higher HP (100 Hz vs 80) and proximity boost at 400 Hz "
              "instead of 250 Hz — female F0 sits an octave higher so the warmth band shifts up.",
    ),

    "ELI": VoiceProfile(
        ceo="ELI",
        f0_range_hz=(95, 160),
        wpm_target=160,
        eq_bands=[
            EQBand("highpass", 80,   0,   0.707),
            EQBand("peak",     280,  3.0, 1.0),    # warm body for blue-collar
            EQBand("peak",     3800, 2.5, 1.0),
            EQBand("peak",     12000, 2.0, 0.8),
        ],
        compression=Compression(ratio=4.0, threshold_db=-17.0, attack_ms=10, release_ms=70),
        reverb=Reverb(predelay_ms=40, decay_s=0.4, wet_db=-18),  # intimate working-class
        lufs_target=-15.0,
        sonic_logo="eli-abundantly-blessed",
        mood_tag="high-energy blue-collar NYC hustle",
        notes="⚠️ ELI IS A REAL PERSON (Edwin's client). This profile is only applied if Edwin "
              "secures Eli's explicit consent to clone his voice. Fast energetic profile matches "
              "his actual NYC entrepreneur register.",
    ),
}


def get(ceo: str) -> VoiceProfile:
    """Look up a voice profile by CEO name (case-insensitive)."""
    key = ceo.upper()
    if key not in PROFILES:
        raise KeyError(
            f"No voice profile for {ceo!r}. Known: {sorted(PROFILES.keys())}"
        )
    return PROFILES[key]


def all_profiles() -> list[VoiceProfile]:
    return list(PROFILES.values())
