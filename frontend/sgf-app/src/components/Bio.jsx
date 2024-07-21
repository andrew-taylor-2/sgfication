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
    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum vestibulum.",
    img: "../../public/biopics/pic1.png",
  },
  {
    text: "Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin.",
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


