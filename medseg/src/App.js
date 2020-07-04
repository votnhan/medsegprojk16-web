import React from 'react';
import logo from './logo.svg';
import './styles/App.css';
import HomePage from './components/HomePage/HomePage';

class App extends React.Component {
  state = { myLink: '' };

  render() {
    return (
      <div>
        <HomePage />
      </div>
    );
  }
}

export default App;
