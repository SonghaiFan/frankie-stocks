/// <reference types="vite/client" />
import {
  HeadContent,
  Scripts,
  createRootRoute,
} from '@tanstack/react-router'
import * as React from 'react'
import { DefaultCatchBoundary } from '~/components/DefaultCatchBoundary'
import { NotFound } from '~/components/NotFound'
import appCss from '~/styles/app.css?url'

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: 'utf-8' },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1',
      },
      {
        title: 'Frank Stocks',
      },
      {
        name: 'description',
        content: 'A TanStack Start stock watchlist and horizon-style return dashboard.',
      },
    ],
    links: [{ rel: 'stylesheet', href: appCss }],
  }),
  errorComponent: DefaultCatchBoundary,
  notFoundComponent: () => <NotFound />,
  shellComponent: RootDocument,
})

function RootDocument({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <HeadContent />
      </head>
      <body>
        {children}
        <footer style={{ textAlign: "center", padding: 16, color: "#61746e" }}><a href="https://songhaifan.github.io/frankie-stocks/" aria-label="About Frankie stocks" style={{ display: "inline-flex", alignItems: "center", padding: "6px", color: "inherit",  }}><span aria-hidden="true" style={{ display: "block", width: 76, height: 26, backgroundColor: "currentColor", mask: "url(/frankie-signature.svg) center / contain no-repeat", WebkitMask: "url(/frankie-signature.svg) center / contain no-repeat" }} /></a></footer>
        <Scripts />
      </body>
    </html>
  )
}
