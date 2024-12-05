import fbapp from "../firebase/firebaseConfig";
import CryptoButton from "./CryptoButton";
import { columns } from "./payments/columns";
import { DataTable } from "./payments/data-table";
import { useState, useEffect } from "react";
import { getDatabase, ref, onValue } from "firebase/database";

import { Skeleton } from "@/components/ui/skeleton";

//TODO: Grab Name and sentiment from FireBase

const CryptoButtons = () => {
  // https://samuelbankole.medium.com/google-firebase-in-react-1acc64516788
  const [data, setData] = useState([]);

  useEffect(() => {
    const database = getDatabase(fbapp);

    const databaseRef = ref(database);

    const fetchData = () => {
      onValue(databaseRef, (snapshot) => {
        const dataItem = snapshot.val();

        if (dataItem) {
          const item = Object.entries(dataItem);

          // console.log(item)

          let list_of_crypto = [];

          for (let i = 0; i < item.length; i++) {
            let name = item[i][0];

            let crypto_data = item[i][1];
            let dates = Object.keys(crypto_data);

            dates.sort((a, b) => new Date(b) - new Date(a));

            let latest_date = dates[0];

            let sent_scores = [];
            for (const key in crypto_data[latest_date]) {
              sent_scores.push(crypto_data[latest_date][key].sentiment);
            }
            let avg_sent_score =
              sent_scores.reduce((a, b) => a + b) / sent_scores.length;

            avg_sent_score = avg_sent_score.toFixed(1);

            list_of_crypto.push({
              id: `${i}`,
              sentiment: avg_sent_score,
              crypto: (
                <CryptoButton
                  name={`${name}`}
                  latest_sent_score={`${avg_sent_score}`}
                  info={crypto_data}
                />
              ),
            });
          }

          setData(list_of_crypto);
        }
      });
    };
    fetchData();
  }, []);
  let content;
  
  if (data.length != 0) {
    content = <DataTable columns={columns} data={data} />;
  } else {
    content = (
      <div className="flex flex-col space-y-3">
        <Skeleton className="h-[125px] w-[320px] rounded-xl" />
        <div className="space-y-2">
          <Skeleton className="h-4 w-[250px]" />
          <Skeleton className="h-4 w-[200px]" />
        </div>
      </div>
    );
  }

  return <>{content}</>;
};

export default CryptoButtons;
