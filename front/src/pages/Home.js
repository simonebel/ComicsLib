import { Box } from "@mui/system";
import { useTitle } from "./page";
import SearchBar from "../components/searchBar";
import {
	Button,
	Card,
	CardActionArea,
	CardActions,
	CardContent,
	CardMedia,
	Grid,
	TextField,
	Typography,
} from "@mui/material";
import { Navigate } from "react-router-dom";
import React from "react";
import { useNavigate } from "react-router-dom";
import BaseButton, { AddButton } from "../components/button";
import BasicDialog from "../components/dialog";

const createComics = (
	id,
	title,
	generalSynopsis,
	existingDate,
	numberSynopsis,
	scenario,
	drawers,
	colors,
	editor,
	genre,
	publishedDate,
	image,
) => {
	return {
		id,
		title,
		generalSynopsis,
		existingDate,
		numberSynopsis,
		scenario,
		drawers,
		colors,
		editor,
		genre,
		publishedDate,
		image,
	};
};

const generateData = () => {
	let data = [];
	for (let i = 0; i < 18; i++) {
		data.push(
			createComics(
				i,
				"Le Grand Bug",
				"Imaginez un monde sans internet et toutes les conséquences que cela pourrait entrainer !",
				"1980-today",
				"Un grand bug a affecté Internet. Depuis, le réseau est devenu très instable. Tout étant interconnecté, les problèmes peuvent surgir partout, et à tout moment. Face à l’ampleur du problème, de nombreuses équipes sont mobilisées.Octo++, un groupe d’intervention constitué de Léna, Tom, Lou et Gabriel, est responsable du réseau de transport, sur lequel un tramway et un train fous sont lancés à pleine vitesse.Vont-ils parvenir à résoudre et corriger le problème, trouver des parades, tout en portant assistance aux personnes touchées par ces défaillances ?",
				"Tixier (Jean-Christophe)",
				"Pierpaoli (Roberta)",
				"Amici (Davide)",
				"Jungle",
				"Policier/Thriller, Jeunesse, BD",
				"02 Novembre 2023",
				"",
			),
		);
	}
	return data;
};

function ComicItem({ comicData }) {
	const [shouldNavigate, setShouldNavigate] = React.useState(false);

	const handleClick = () => {
		setShouldNavigate(true);
	};

	return (
		<Grid item sx={{ mt: 4 }} xs={2}>
			<CardActionArea onClick={handleClick}>
				<CardMedia
					component="img"
					image="/static/img/73862-couverture-bd-le-grand-bug-tome-1.jpg"
					alt={comicData.title}
				/>
				<CardContent>
					<Typography gutterBottom variant="h5" component="div">
						{comicData.title}
					</Typography>
					<Typography variant="body2" color="text.secondary">
						{comicData.generalSynopsis}
					</Typography>
				</CardContent>
				{shouldNavigate ? (
					<Navigate to={`/comic/${comicData.id}`}></Navigate>
				) : null}
			</CardActionArea>
		</Grid>
	);
}

function ComicsContainer() {
	let comics = generateData();
	return (
		<Box>
			<Grid container spacing={2}>
				{comics
					? comics.map((comic) => <ComicItem comicData={comic}></ComicItem>)
					: null}
			</Grid>
		</Box>
	);
}

function CreateComic() {
	const [open, setOpen] = React.useState(false);

	const handleClick = () => {
		setOpen(true);
	};

	return (
		<Box>
			<AddButton sx={{ ml: 4 }} onClick={handleClick}></AddButton>
			<BasicDialog
				open={open}
				onClose={() => setOpen(false)}
				title={"Add a Comic"}
			>
				<TextField id="standard-basic" label="Title" variant="standard" />
			</BasicDialog>
		</Box>
	);
}

export default function Home() {
	const { setTitle } = useTitle();
	setTitle("Comics");

	return (
		<Box>
			<Box sx={{ display: "flex" }}>
				<SearchBar></SearchBar>
				<CreateComic></CreateComic>
			</Box>

			<ComicsContainer></ComicsContainer>
		</Box>
	);
}
