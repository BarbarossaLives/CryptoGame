import React, { useEffect, useState } from 'react';
import { getSimplePrices } from '../services/api';

function Dashboard() {
  const [prices, setPrices] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSimplePrices()
      .then(setPrices)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading prices...</div>;

  return (
    <div>
      <h1>Crypto Prices</h1>
      <ul>
        {Object.entries(prices).map(([coin, data]) => (
          <li key={coin}>
            {coin}: ${data.USD.toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
