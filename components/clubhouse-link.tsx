import type { ComponentPropsWithoutRef } from "react";

export function ClubhouseLink({ href, children, ...props }: ComponentPropsWithoutRef<"a"> & { href: string }) {
  return <a href={href} {...props}>{children}</a>;
}
