import { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown } from "lucide-react"

export type Payment = {
  id: string
  amount: number
  status: "pending" | "processing" | "success" | "failed"
  email: string
}

import * as React from "react"
import { Button } from "../ui/button"

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
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() !== "desc")}
        >
          Sentiment
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    // header: () => <div className="text-center">Sentiment</div>,
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
