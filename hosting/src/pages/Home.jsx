import React from 'react'
import CryptoButtons from "../components/CryptoButtons";


const Home = () => {
  return (
    <>
    <div>
        Crypto Board
      </div>
      <div className='m-10'>
        <CryptoButtons/>
      </div>
      <div>
        FootNote
      </div>
    </>
  )
}

export default Home;