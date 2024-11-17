import React from 'react'
import { useParams } from 'react-router-dom';

const CryptoPage = () => {

    const { name } = useParams();

  return (
    <div>{name}</div>
  )
}

export default CryptoPage