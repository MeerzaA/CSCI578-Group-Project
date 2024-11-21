import CryptoButton from "./CryptoButton"

//TODO: Grab Name and sentiment from FireBase

const CryptoButtons = () => {
  return (
    <>
      <CryptoButton name="Bitcoin" sentScore="6"/>
      <CryptoButton name="Ethereum" sentScore="1"/>
    </> 
  )
}

export default CryptoButtons