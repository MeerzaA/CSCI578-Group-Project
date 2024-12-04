import React from 'react'
import CryptoButtons from "../components/CryptoButtons";


const Home = () => {
  return (
    <>
    <div className="m-5 text-center">
        Crypto Board
      </div>
      <div className="m-5 w-80 mx-auto">
        <CryptoButtons/>
      </div>
    </>
  )
}

export default Home;