import fbapp from "../firebase/firebaseConfig";
import CryptoButton from "./CryptoButton";
import { columns } from "./payments/columns";
import { DataTable } from "./payments/data-table";
import { useState, useEffect } from "react";
import { getDatabase, ref, onValue } from "firebase/database";

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

          let list_of_crypto = []

          for (let i=0; i < item.length; i++){
            let crypto_dates = []
            for (let j=0; j < item[i][1].length; j++){
              if (item[i][1][j] === undefined){
                continue;
              }
              let sentiment = item[i][1][j].Sentiment;
              let date = item[i][1][j].date;
              let name = item[i][0];

              crypto_dates.push({sentiment: sentiment,
                date: date,
                name: name
              })

            }
            crypto_dates.sort((a, b) => new Date(b.date) - new Date(a.date));
            list_of_crypto.push({
              id: `${i}`,
              sentiment: crypto_dates[0].sentiment,
              date: crypto_dates[0].date,
              crypto: <CryptoButton name={`${crypto_dates[0].name}`} sentScore={`${crypto_dates[0].sentiment}`}/>
            })
            
          }
          setData(list_of_crypto);
        }
      });
    };
    fetchData();
  }, []);

//   const [data, setData] = useState([{
//     id: "728ed52f",
//     sentiment: 6,
//     crypto: <CryptoButton name="Bitcoin" sentScore="6"/>,
//   },
// {
//     id: "214234d",
//     sentiment: 2,
//     crypto: <CryptoButton name="Ethereum" sentScore="2"/>,
//   }]);


return (
  <>
  <DataTable columns={columns} data={data} />
  </> 
)
}

export default CryptoButtons