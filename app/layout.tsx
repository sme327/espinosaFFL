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
  // Tab icon: a Fredoka "E" in action green on stadium navy, rendered to PNG/ICO (the old
  // favicon.svg was an emoji in a <text> element, which the stadium contract forbids).
  icons: { icon: [{ url: "/favicon.ico", sizes: "any" }, { url: "/favicon-32.png", sizes: "32x32", type: "image/png" }, { url: "/icon-512.png", sizes: "512x512", type: "image/png" }], shortcut: "/favicon.ico", apple: "/apple-touch-icon.png" },
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
