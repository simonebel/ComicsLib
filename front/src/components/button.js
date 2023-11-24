import { Button, IconButton } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { blue } from "@mui/material/colors";
import styled from "@emotion/styled";

export default function BaseButton() {
	return <Button variant="contained">Contained</Button>;
}

const HoverButton = styled(IconButton)({
	background: blue[700],
	"&:hover": {
		background: blue[900],
	},
});

export function AddButton({ sx, onClick }) {
	return (
		<HoverButton sx={sx} onClick={onClick}>
			<AddIcon sx={{ color: "white" }}></AddIcon>
		</HoverButton>
	);
}
