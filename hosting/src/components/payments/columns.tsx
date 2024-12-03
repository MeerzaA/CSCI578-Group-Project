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
    header: () => <div className="text-center">Sentiment</div>,
    cell: ({ row }) => {
      let sent = parseFloat(row.getValue("sentiment"))
      if (sent > 7){
        return <div  className="text-center text-green-600 font-medium">{row.getValue("sentiment")}</div>
      }
      else if (sent < 4){
        return <div  className="text-center text-red-600 font-medium">{row.getValue("sentiment")}</div>
      }
      else{
        return <div  className="text-center text-yellow-600 font-medium">{row.getValue("sentiment")}</div>
      }
    },

  },
]
