import type { Metadata } from "next";
import { Fredoka, Nunito } from "next/font/google";
import "./globals.css";
import { SiteHeader } from "@/components/site-header";

const fredoka = Fredoka({ variable: "--font-display", subsets: ["latin"] });
const nunito = Nunito({ variable: "--font-sans", subsets: ["latin"] });
const description = "A family fantasy football museum — every champion, every rivalry, every season since 2023.";

export const metadata: Metadata = {
  metadataBase: new URL("https://espinosaFFL.sme327.com"),
  title: { default: "Espinosa FFL Clubhouse", template: "%s · Espinosa FFL" },
  description,
  icons: { icon: "/favicon.svg", shortcut: "/favicon.svg" },
  openGraph: { title: "Espinosa FFL Clubhouse", description },
  twitter: { card: "summary", title: "Espinosa FFL Clubhouse", description },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${fredoka.variable} ${nunito.variable}`}>
        <SiteHeader />
        {children}
        {/* Cloudflare Web Analytics — plain script tag, same as the Dynasty 22
            museum on this identical vinext/Workers stack; next/script's
            afterInteractive strategy isn't something vinext's shim guarantees. */}
        <script
          type="module"
          src="https://static.cloudflareinsights.com/beacon.min.js"
          data-cf-beacon='{"token":"ad0732a55dae401bb2525a628d387dd0"}'
        ></script>
        {/* End Cloudflare Web Analytics */}
      </body>
    </html>
  );
}
