import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./pages/Home";
import Page from "./pages/page";
import Comic from "./pages/Comic";

{
	/* <Route path="/" element={<Page />}>
<Route path="/" element={<Home />}></Route>
<Route path="comic">
  <Route path=":comicID" element={<Comic />}></Route>
</Route> */
}

const router = createBrowserRouter([
	{
		path: "/",
		element: <Page />,
		children: [
			{
				path: "/",
				element: <Home />,
			},
			{
				path: "/comic",
				children: [{ path: ":comicID", element: <Comic /> }],
			},
		],
	},
]);

function App() {
	return <RouterProvider router={router} />;
}

export default App;
