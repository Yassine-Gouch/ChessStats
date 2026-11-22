import Sidebar from "../components/Sidebar";

function MainLayout({ children }) {
  return (
    <div className="flex min-h-screen bg-[#0B1220]">

      <Sidebar />

      <main className="flex-1 p-10">
        {children}
      </main>

    </div>
  );
}

export default MainLayout;
