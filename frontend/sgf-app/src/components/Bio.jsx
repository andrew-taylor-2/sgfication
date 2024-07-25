import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import { GlobalStyles } from '@mui/material';

const globalStyles = (
  <GlobalStyles
    styles={{
      body: {
        backgroundColor: '#646464', // Background color for the body
        margin: 0,
        padding: 0,
        fontFamily: 'Roboto, sans-serif',
      },
    }}
  />
);

const content = [
  
  {
    img: "../../public/biopics/pic0.png",
    fullWidth: true,
  },
  {
    text: "Hi, I'm Andrew Taylor! Based in Atlanta, I have been finding solutions in medical image analysis, whether that is statistical analysis, complex image manipulations, generalizing and updating legacy code, or leveraging the field's cutting-edge software tools. I've especially enjoyed finding difficult technical solutions, which has led me to pivot into seeking out software development roles.",
    fullWidth: true,
  },
  {
    text: "For the last 4 years I've conducted brain research in NASA astronauts and in terrestrial spaceflight analogues. This has resulted in my authorship on 4 papers and presentation at NASA's Human Research Program Investigator's Workshop. \n \nblahhhh",
    img: "../../public/biopics/braingif.gif",
  },
  {
    text: "",
    img: "../../public/biopics/pic2.png",
  },
  {
    text: "This is a longer text section that spans the full width of the container. You can use this section to provide more detailed information or any other content that requires more space.",
    fullWidth: true,
  },
  {}, // this is to fix the modulo 2 so that the pics still zig zag
  {
    text: "Maecenas sed diam eget risus varius blandit sit amet non magna.",
    img: "../../public/biopics/pic3.png",
  },
  {
    text: "Curabitur blandit tempus porttitor. Integer posuere erat a ante venenatis dapibus posuere velit aliquet.",
    img: "../../public/biopics/pic2.png",
  },
];

const Bio = () => {
  return (
    <>
      {globalStyles}
      <Container maxWidth="lg" sx={{ padding: '2rem 0' }}> 
        {content.map((item, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              flexDirection: item.fullWidth ? 'column' : index % 2 === 0 ? 'row' : 'row-reverse',
              alignItems: item.fullWidth ? 'center' : 'center',
              marginBottom: '2rem',
            }}
          >
            {item.img && (
              <Box
                component="img"
                src={item.img}
                alt={`Image ${index + 1}`}
                sx={{
                  width: '75%',
                  height: 'auto',
                  borderRadius: '8px',
                  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                  marginRight: index % 2 === 0 ? '1rem' : '0',
                  marginLeft: index % 2 === 0 ? '0' : '1rem',
                }}
              />
            )}
            <Typography
              variant="body1"
              sx={{ 
                width: item.fullWidth ? '100%' : '50%', 
                color: '#fff', 
                padding: '1rem', 
                textAlign: item.fullWidth ? 'center' : 'left',
              }}
            >
              {item.text}
            </Typography>
          </Box>
        ))}
      </Container>
    </>
  );
};

export default Bio;


