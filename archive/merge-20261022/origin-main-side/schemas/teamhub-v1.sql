-- TeamHub schema v1, generated 2026-10-18 17:12

CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE agents(
  id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, name TEXT, role TEXT,
  model TEXT, workspace TEXT, notes TEXT);
CREATE TABLE projects(
  id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, name TEXT, category TEXT,
  status TEXT, lead_agent TEXT, support_agents TEXT, description TEXT,
  repo_path TEXT, board_path TEXT, created_at TEXT, updated_at TEXT);
CREATE TABLE project_categories(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, code TEXT, name TEXT, description TEXT);
CREATE TABLE workflow_steps(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, step_no INTEGER, name TEXT,
  owner_agent TEXT, input_desc TEXT, output_desc TEXT, status TEXT, note TEXT);
CREATE TABLE sources(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, category TEXT, title TEXT, url TEXT,
  platform TEXT, author TEXT, published TEXT, collected_at TEXT, collected_by TEXT,
  reliability TEXT, status TEXT, note TEXT);
CREATE TABLE resources(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, url TEXT, kind TEXT,
  found_in TEXT, found_by TEXT, status TEXT, note TEXT);
CREATE TABLE documents(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, owner TEXT, title TEXT, path TEXT,
  doc_type TEXT, date TEXT, size_bytes INTEGER, summary TEXT, status TEXT);
CREATE TABLE artifacts(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, name TEXT, path TEXT, type TEXT,
  version TEXT, checksum TEXT, status TEXT, description TEXT);
CREATE TABLE findings(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, topic TEXT, claim TEXT, evidence TEXT,
  confidence TEXT, source_ref TEXT, tags TEXT, status TEXT, created_at TEXT);
CREATE TABLE params(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, category TEXT, item TEXT, value TEXT,
  unit TEXT, status TEXT, source_ref TEXT, note TEXT);
CREATE TABLE decisions(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, title TEXT, decision TEXT,
  rationale TEXT, alternatives TEXT, decided_by TEXT, decided_at TEXT, status TEXT);
CREATE TABLE tasks(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, title TEXT, description TEXT,
  owner TEXT, priority TEXT, status TEXT, write_scope TEXT, blocked_by TEXT,
  created_at TEXT, updated_at TEXT);
CREATE TABLE handoffs(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, marker TEXT, from_agent TEXT,
  to_agent TEXT, path TEXT, status TEXT, date TEXT, note TEXT);
CREATE TABLE reviews(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, target TEXT, reviewer TEXT,
  result TEXT, notes TEXT, date TEXT);
CREATE TABLE events(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, at TEXT, agent TEXT, action TEXT, detail TEXT);
CREATE TABLE entity_links(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, from_type TEXT, from_id INTEGER,
  to_type TEXT, to_id INTEGER, relation TEXT);
-- 域扩展表：疯狂电路
CREATE TABLE x_teams(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, event TEXT, edition TEXT, year INTEGER,
  region TEXT, rank_no INTEGER, school TEXT, team_name TEXT, award TEXT,
  score_prelim TEXT, score_final TEXT, advisor1 TEXT, advisor2 TEXT,
  student1 TEXT, student2 TEXT, student3 TEXT, note TEXT);
CREATE TABLE x_repos(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, platform TEXT, owner TEXT, name TEXT,
  url TEXT, linked_school TEXT, linked_team TEXT, award_claim TEXT, mcu TEXT, driver TEXT,
  camera TEXT, imu TEXT, content_summary TEXT, app_files INTEGER, app_lines INTEGER,
  last_commit TEXT, verified TEXT, license TEXT, local_path TEXT, note TEXT);
CREATE TABLE x_videos(
  bvid TEXT PRIMARY KEY, project_id INTEGER, title TEXT, up TEXT, aid INTEGER,
  view_count INTEGER, comment_count INTEGER, pubdate TEXT, desc_text TEXT, note TEXT);
CREATE TABLE x_comments(
  id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER, bvid TEXT, user TEXT,
  content TEXT, like_count INTEGER, is_reply INTEGER);
