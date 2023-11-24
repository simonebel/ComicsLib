import { Box } from "@mui/system";
import { Outlet, useOutletContext } from "react-router-dom";
import MenuDrawer from "../components/Menu";
import { blue } from "@mui/material/colors";
import { Typography } from "@mui/material";
import React from "react";

export default function Page() {
	const [title, setTitle] = React.useState("");
	return (
		<Box sx={{ display: "flex" }}>
			<MenuDrawer></MenuDrawer>
			<Box>
				<Box
					sx={{
						mb: 2,
						backgroundColor: blue[900],
						width: "80vw",
						height: "18vh",
					}}
				>
					<Typography variant="h3" sx={{ p: 4 }}>
						{title}
					</Typography>
				</Box>
				<Box sx={{ p: 4 }}>
					<Outlet context={{ setTitle }} />
				</Box>
			</Box>
		</Box>
	);
}

export function useTitle() {
	return useOutletContext();
}
