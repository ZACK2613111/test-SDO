import Link from "next/link";
import { styled } from "@mui/material";
import Image from "next/image";

const LinkStyled = styled(Link)(() => ({
  height: "70px",
  width: "180px",
  overflow: "hidden",
  display: "block",
}));

const Logo = () => {
  return (
    <LinkStyled href="https://smartdrillingops.com" target="_blank">
      <Image src="/images/logos/Logo.jpeg" alt="logo" height={74} width={190} priority />
    </LinkStyled>
  );
};

export default Logo;
