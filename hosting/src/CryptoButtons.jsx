import CryptoButton from "./CryptoButton"

//TODO: Grab Name and sentiment from FireBase

const CryptoButtons = () => {
  return (
    <>
      <CryptoButton name="BitCoin" sentScore="6"/>
      <CryptoButton name="DogeCoin" sentScore="1"/>
    </> 
  )
}

export default CryptoButtons