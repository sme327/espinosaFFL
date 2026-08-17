import vinext from "vinext";
import { defineConfig } from "vite";

const CLUBHOUSE_D1_DATABASE_ID = "bb3406d9-aa95-45ae-8364-7de55f7df574";

export default defineConfig(async () => {
  const { cloudflare } = await import("@cloudflare/vite-plugin");

  return {
    plugins: [
      vinext(),
      cloudflare({
        viteEnvironment: { name: "rsc", childEnvironments: ["ssr"] },
        config: {
          main: "./worker/index.ts",
          compatibility_flags: ["nodejs_compat"],
          d1_databases: [{ binding: "DB", database_name: "espinosa-ffl-clubhouse", database_id: CLUBHOUSE_D1_DATABASE_ID }],
          routes: [{ pattern: "espinosaFFL.sme327.com", custom_domain: true }],
        },
      }),
    ],
  };
});
