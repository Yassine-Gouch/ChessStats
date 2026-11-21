import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Players from "./pages/Players";
import Predict from "./pages/Predict";
import Openings from "./pages/Openings";
import Tournaments from "./pages/Tournaments";
import PlayerProfile from "./pages/PlayerProfile";
import Compare from "./pages/Compare";

function App() {
  return (
    <BrowserRouter>

      <MainLayout>

        <Routes>

          <Route path="/" element={<Dashboard />} />

          <Route path="/players" element={<Players />} />

          <Route path="/compare" element={<Compare />} />

          <Route path="/predict" element={<Predict />} />

          <Route path="/openings" element={<Openings />} />

          <Route
            path="/tournaments"
            element={<Tournaments />}

            
          />

          <Route path="/player/:name" element={<PlayerProfile />} />
          

        </Routes>

      </MainLayout>

    </BrowserRouter>
  );
}

export default App;