const API_URL = "https://chessstats-jwakvg.fly.dev";
export async function getInfo() {

  const response = await fetch(
    `${API_URL}/info`
  );

  return await response.json();
}

export async function searchPlayers(query) {
  const response = await fetch(
    `${API_URL}/players/search?q=${query}`
  );

  return await response.json();
}

export async function getPlayerRatingHistory(name) {
  const response = await fetch(
    `${API_URL}/players/rating-history/${name}`
  );

  return await response.json();
}

export async function getPlayerOpenings(name) {
  const response = await fetch(
    `${API_URL}/players/openings/${name}`
  );

  return await response.json();
}

export async function getOpeningsStats() {
  const response = await fetch(
    `${API_URL}/openings/stats`
  );

  return await response.json();
}

export async function getTopOpenings() {
  const response = await fetch(
    `${API_URL}/openings/top`
  );

  return await response.json();
}

export async function getOpeningDetails(eco) {
  const response = await fetch(
    `${API_URL}/openings/${eco}`
  );

  return await response.json();
}

export async function getOpeningTopPlayer(eco) {
  const response = await fetch(
    `${API_URL}/openings/${eco}/top-player`
  );

  return await response.json();
}

export async function getTournamentsStats() {

  const response = await fetch(
    `${API_URL}/tournaments/stats`
  );

  return await response.json();
}

export async function getTopTournaments() {

  const response = await fetch(
    `${API_URL}/tournaments/top`
  );

  return await response.json();
}

export async function getTournamentDetails(
  event,
  year
) {

  const response = await fetch(
    `${API_URL}/tournaments/${year}/${encodeURIComponent(event)}`
  );

  return await response.json();
}