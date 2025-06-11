import React from 'react';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <div className="App">
      <header style={{ padding: '1rem', backgroundColor: '#282c34', color: 'white' }}>
        <h1>Crypto Trading Sim</h1>
      </header>
      <main style={{ padding: '1rem' }}>
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
