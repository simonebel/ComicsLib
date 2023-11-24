import { Box, TextField } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

export default function SearchBar() {
	return (
		<Box
			sx={{
				border: 1,
				borderRadius: 2,
				width: "100%",
				display: "flex",
				alignItems: "center",
			}}
		>
			<SearchIcon sx={{ height: "100%", p: 1 }}></SearchIcon>
			<TextField
				id="input-search"
				variant="standard"
				InputProps={{ disableUnderline: true }}
				placeholder="Search a comic"
			/>
		</Box>
	);
}
