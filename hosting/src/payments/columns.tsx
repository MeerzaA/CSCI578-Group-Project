import { ColumnDef } from "@tanstack/react-table"

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Payment = {
  id: string
  amount: number
  status: "pending" | "processing" | "success" | "failed"
  email: string
}

import * as React from "react"

export const columns: ColumnDef<Payment>[] = [
  {
    accessorKey: "crypto",
    header: "Crypto",
    cell: ({ row }) => {
      return <div  className="text-left font-medium">{row.getValue('crypto')}</div>
    }
  },
  {
    accessorKey: "sentiment",
    header: () => <div className="text-left">Sentiment</div>,
    cell: ({ row }) => {
      return <div  className="text-left font-medium">{row.getValue("sentiment")}</div>
    },

  },
]
