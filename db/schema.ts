// Each entry is exactly one SQLite statement so D1 can execute it safely with
// DB.prepare(statement).run() or batch prepared statements during setup.
export const DRAFT_SCHEMA_STATEMENTS = [
  `CREATE TABLE IF NOT EXISTS draft_managers (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    pin_hash TEXT NOT NULL,
    is_commissioner INTEGER NOT NULL DEFAULT 0 CHECK (is_commissioner IN (0, 1)),
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )`,
  `CREATE TABLE IF NOT EXISTS draft_seasons (
    id TEXT PRIMARY KEY,
    season INTEGER NOT NULL UNIQUE,
    family_size INTEGER NOT NULL CHECK (family_size = 5),
    status TEXT NOT NULL DEFAULT 'planning',
    order_type TEXT NOT NULL CHECK (order_type IN ('snake', 'linear')),
    rounds INTEGER NOT NULL CHECK (rounds > 0),
    roster_slots_json TEXT NOT NULL,
    commissioner_manager_id TEXT NOT NULL REFERENCES draft_managers(id),
    current_overall INTEGER NOT NULL DEFAULT 1,
    version INTEGER NOT NULL DEFAULT 1,
    started_at TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )`,
  `CREATE TABLE IF NOT EXISTS draft_teams (
    id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL REFERENCES draft_seasons(id),
    manager_id TEXT NOT NULL REFERENCES draft_managers(id),
    team_name TEXT NOT NULL,
    draft_position INTEGER,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(draft_id, manager_id),
    UNIQUE(draft_id, draft_position)
  )`,
  `CREATE TABLE IF NOT EXISTS draft_players (
    id TEXT PRIMARY KEY,
    season INTEGER NOT NULL,
    source TEXT NOT NULL,
    source_id TEXT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    nfl_team TEXT,
    bye_week INTEGER,
    overall_rank INTEGER,
    image_url TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(season, source, source_id)
  )`,
  `CREATE TABLE IF NOT EXISTS draft_slots (
    id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL REFERENCES draft_seasons(id),
    overall INTEGER NOT NULL,
    round INTEGER NOT NULL,
    pick_in_round INTEGER NOT NULL,
    team_id TEXT NOT NULL REFERENCES draft_teams(id),
    roster_slot TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(draft_id, overall),
    UNIQUE(draft_id, round, pick_in_round)
  )`,
  `CREATE TABLE IF NOT EXISTS draft_picks_live (
    id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL REFERENCES draft_seasons(id),
    slot_id TEXT NOT NULL REFERENCES draft_slots(id),
    player_id TEXT NOT NULL REFERENCES draft_players(id),
    team_id TEXT NOT NULL REFERENCES draft_teams(id),
    actor_manager_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    selection_type TEXT NOT NULL DEFAULT 'manager' CHECK (selection_type IN ('manager', 'commissioner_proxy')),
    override_reason TEXT,
    reversed_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(draft_id, idempotency_key)
  )`,
  `CREATE UNIQUE INDEX IF NOT EXISTS idx_draft_picks_active_slot
    ON draft_picks_live(draft_id, slot_id) WHERE reversed_at IS NULL`,
  `CREATE UNIQUE INDEX IF NOT EXISTS idx_draft_picks_active_player
    ON draft_picks_live(draft_id, player_id) WHERE reversed_at IS NULL`,
  `CREATE INDEX IF NOT EXISTS idx_draft_players_season_position
    ON draft_players(season, position)`,
  `CREATE INDEX IF NOT EXISTS idx_draft_slots_team
    ON draft_slots(draft_id, team_id)`,
  `CREATE TABLE IF NOT EXISTS draft_events (
    id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL REFERENCES draft_seasons(id),
    sequence INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    actor_manager_id TEXT,
    idempotency_key TEXT,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(draft_id, sequence)
  )`,
  `CREATE INDEX IF NOT EXISTS idx_draft_events_type
    ON draft_events(draft_id, event_type)`,
  `CREATE TABLE IF NOT EXISTS draft_snapshots (
    id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL REFERENCES draft_seasons(id),
    event_sequence INTEGER NOT NULL,
    state_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(draft_id, event_sequence)
  )`,
  `CREATE TABLE IF NOT EXISTS draft_transitions (
    id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL REFERENCES draft_seasons(id),
    from_version INTEGER NOT NULL,
    to_version INTEGER NOT NULL,
    idempotency_key TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(draft_id, from_version),
    UNIQUE(draft_id, idempotency_key)
  )`,
  `CREATE TABLE IF NOT EXISTS draft_sessions (
    id TEXT PRIMARY KEY,
    manager_id TEXT NOT NULL REFERENCES draft_managers(id),
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TEXT NOT NULL,
    revoked_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )`,
  `CREATE INDEX IF NOT EXISTS idx_draft_sessions_manager
    ON draft_sessions(manager_id, expires_at)`,
  `CREATE TABLE IF NOT EXISTS draft_login_limits (
    key TEXT PRIMARY KEY,
    failed_count INTEGER NOT NULL DEFAULT 0,
    window_started_at TEXT NOT NULL,
    blocked_until TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )`,
] as const;

export const CLUBHOUSE_SCHEMA_STATEMENTS = [
  `CREATE TABLE IF NOT EXISTS clubhouse_events (
    id TEXT PRIMARY KEY,
    season INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    manager_id TEXT,
    occurred_at TEXT NOT NULL,
    source TEXT NOT NULL CHECK (source IN ('league', 'draft', 'weekly', 'commissioner')),
    source_id TEXT,
    title TEXT NOT NULL,
    story TEXT,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, source_id)
  )`,
  `CREATE INDEX IF NOT EXISTS idx_clubhouse_events_season_type
    ON clubhouse_events(season, event_type, occurred_at)`,
  `CREATE INDEX IF NOT EXISTS idx_clubhouse_events_manager
    ON clubhouse_events(manager_id, occurred_at)`,
  `CREATE TABLE IF NOT EXISTS achievement_definitions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    icon TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('league', 'draft', 'participation', 'family_spirit', 'memory')),
    award_method TEXT NOT NULL CHECK (award_method IN ('automatic', 'commissioner')),
    repeatable INTEGER NOT NULL DEFAULT 0 CHECK (repeatable IN (0, 1)),
    rule_key TEXT,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    sort_order INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )`,
  `CREATE TABLE IF NOT EXISTS achievement_awards (
    id TEXT PRIMARY KEY,
    achievement_id TEXT NOT NULL REFERENCES achievement_definitions(id),
    manager_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    award_key TEXT NOT NULL,
    event_id TEXT REFERENCES clubhouse_events(id),
    awarded_by_manager_id TEXT,
    awarded_at TEXT NOT NULL,
    note TEXT,
    photo_url TEXT,
    revoked_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )`,
  `CREATE INDEX IF NOT EXISTS idx_achievement_awards_manager_season
    ON achievement_awards(manager_id, season, awarded_at)`,
  `CREATE UNIQUE INDEX IF NOT EXISTS idx_achievement_awards_once
    ON achievement_awards(achievement_id, manager_id, award_key)
    WHERE revoked_at IS NULL`,
  `CREATE TABLE IF NOT EXISTS weekly_matchups (
    id TEXT PRIMARY KEY,
    season INTEGER NOT NULL,
    week INTEGER NOT NULL CHECK (week > 0),
    manager_a_id TEXT NOT NULL,
    manager_b_id TEXT NOT NULL,
    locks_at TEXT NOT NULL,
    featured INTEGER NOT NULL DEFAULT 0 CHECK (featured IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (manager_a_id != manager_b_id),
    UNIQUE(season, week, manager_a_id, manager_b_id)
  )`,
  `CREATE INDEX IF NOT EXISTS idx_weekly_matchups_season_week
    ON weekly_matchups(season, week, locks_at)`,
  `CREATE TABLE IF NOT EXISTS weekly_predictions (
    id TEXT PRIMARY KEY,
    matchup_id TEXT NOT NULL REFERENCES weekly_matchups(id),
    participant_manager_id TEXT NOT NULL,
    predicted_manager_id TEXT NOT NULL,
    confidence TEXT NOT NULL CHECK (confidence IN ('unsure', 'confident', 'super')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(matchup_id, participant_manager_id)
  )`,
  `CREATE INDEX IF NOT EXISTS idx_weekly_predictions_participant
    ON weekly_predictions(participant_manager_id, matchup_id)`,
] as const;

export type DraftSchemaStatement = (typeof DRAFT_SCHEMA_STATEMENTS)[number];
export type ClubhouseSchemaStatement = (typeof CLUBHOUSE_SCHEMA_STATEMENTS)[number];
