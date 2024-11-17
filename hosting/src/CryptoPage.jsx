import React from 'react'
import { useParams } from 'react-router-dom';
//TODO: Grab Graph Data Here (frequency from News, Frequency from Social Media, Sentiment over Time)
const CryptoPage = () => {

    const { name } = useParams();

  return (
    <div>{name}</div>
  )
}

export default CryptoPage