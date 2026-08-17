declare module "cloudflare:workers" {
  import type { D1DatabaseLike } from "@/db";
  export const env: { DB: D1DatabaseLike };
}
