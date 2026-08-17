import { CLUBHOUSE_SCHEMA_STATEMENTS, DRAFT_SCHEMA_STATEMENTS } from "./schema";

export type D1ResultSetLike<T> = { results: T[] };
export type D1PreparedStatementLike = {
  bind(...values: unknown[]): D1PreparedStatementLike;
  run(): Promise<unknown>;
  first<T>(): Promise<T | null>;
  all<T>(): Promise<D1ResultSetLike<T>>;
};
export type D1DatabaseLike = {
  prepare(statement: string): D1PreparedStatementLike;
  batch(statements: D1PreparedStatementLike[]): Promise<unknown>;
};

export function requireDraftDb(env: { DB?: D1DatabaseLike }): D1DatabaseLike {
  if (!env.DB) throw new Error("Draft database binding `DB` is unavailable.");
  return env.DB;
}

export async function initializeDraftSchema(db: D1DatabaseLike): Promise<void> {
  await db.batch(DRAFT_SCHEMA_STATEMENTS.map((statement) => db.prepare(statement)));
}

export async function initializeClubhouseSchema(db: D1DatabaseLike): Promise<void> {
  await db.batch(CLUBHOUSE_SCHEMA_STATEMENTS.map((statement) => db.prepare(statement)));
}
