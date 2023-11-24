import { Box } from "@mui/system";
import { blue } from "@mui/material/colors";
import * as React from "react";
import Divider from "@mui/material/Divider";
import MenuList from "@mui/material/MenuList";
import MenuItem from "@mui/material/MenuItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemIcon from "@mui/material/ListItemIcon";
import Typography from "@mui/material/Typography";
import ContentCopy from "@mui/icons-material/ContentCopy";
import ContentPaste from "@mui/icons-material/ContentPaste";
import Cloud from "@mui/icons-material/Cloud";
import MenuBookIcon from "@mui/icons-material/MenuBook";
import { Navigate } from "react-router-dom";
import { Outlet, Link } from "react-router-dom";

function NavigationItem({ text, to }) {
	const [shouldNavigate, setShouldNavigate] = React.useState(false);

	return (
		<Link to={to} style={{ textDecoration: "none", color: "rgb(0, 0, 0)" }}>
			<MenuItem to={to}>
				<ListItemIcon>
					<MenuBookIcon fontSize="small" />
				</ListItemIcon>
				<ListItemText>{text}</ListItemText>
			</MenuItem>
		</Link>
	);
}

export default function MenuDrawer() {
	return (
		<Box sx={{ backgroundColor: blue[500], width: "20vw", height: "100vh" }}>
			<MenuList sx={{ width: "100%" }}>
				<NavigationItem text={"My Comics"} to={"/"}></NavigationItem>
				<MenuItem>
					<ListItemIcon>
						<ContentCopy fontSize="small" />
					</ListItemIcon>
					<ListItemText>Copy</ListItemText>
					<Typography variant="body2" color="text.secondary">
						⌘C
					</Typography>
				</MenuItem>
				<MenuItem>
					<ListItemIcon>
						<ContentPaste fontSize="small" />
					</ListItemIcon>
					<ListItemText>Paste</ListItemText>
					<Typography variant="body2" color="text.secondary">
						⌘V
					</Typography>
				</MenuItem>
				<Divider />
				<MenuItem>
					<ListItemIcon>
						<Cloud fontSize="small" />
					</ListItemIcon>
					<ListItemText
						sx={{ whiteSpace: "normal" }}
						primary={"Web Clipboard"}
					></ListItemText>
				</MenuItem>
			</MenuList>
		</Box>
	);
}
