export async function getOverview() {
  const response = await fetch('/api/overview');
  return response.json();
}
