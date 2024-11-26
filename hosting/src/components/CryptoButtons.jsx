import CryptoButton from "./CryptoButton"

//TODO: Grab Name and sentiment from FireBase


const CryptoButtons = () => {

  const [data, setData] = useState([{
    id: "728ed52f",
    sentiment: 6,
    crypto: <CryptoButton name="Bitcoin" sentScore="6"/>,
  },
{
    id: "214234d",
    sentiment: 1,
    crypto: <CryptoButton name="Ethereum" sentScore="1"/>,
  }]);


return (
  <>
  <DataTable columns={columns} data={data} />
  </> 
)
}

export default CryptoButtons