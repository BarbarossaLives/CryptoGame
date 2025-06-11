const API_BASE = 'https://min-api.cryptocompare.com/data';
const API_KEY = import.meta.env.VITE_CRYPTOCOMPARE_API_KEY;

export async function getSimplePrices(symbols = ['BTC', 'ETH', 'SOL', 'ADA']) {
  const response = await fetch(
    `${API_BASE}/pricemulti?fsyms=${symbols.join(',')}&tsyms=USD`,
    {
      headers: {
        authorization: `Apikey ${API_KEY}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch prices from CryptoCompare');
  }

  return response.json(); // { BTC: { USD: 12345 }, ETH: { USD: 2345 } }
}
