import { Box } from "@mui/system";
import { Outlet } from "react-router-dom";

export default function Page() {
  return (
    <Box>
      <Outlet />
    </Box>
  );
}
