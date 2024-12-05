import React from 'react'
import CryptoButtons from "../components/CryptoButtons";


const Home = () => {
  return (
    <>
    <div className="text-center text-5xl m-11">
        Crypto Board
      </div>
      <div className="m-5 w-80 mx-auto">
        <CryptoButtons/>
      </div>
    </>
  )
}

export default Home;