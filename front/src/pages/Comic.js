import { Box } from "@mui/material";
import { useTitle } from "./page";
import { useParams } from "react-router-dom";

export default function Comic() {
	const { setTitle } = useTitle();
	const params = useParams();
	console.log();
	setTitle(`Comic ${params.comicID}`);

	return <Box></Box>;
}
