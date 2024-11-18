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
    img: "/biopics/pic0.png",
    fullWidth: true,
  },
  {
    text: "Hi, I'm Andrew Taylor! Based in Atlanta, I have been finding solutions in medical image analysis, whether that is statistical analysis, complex image manipulations, generalizing and updating legacy code, or utilizing the lastest software tools in the field. I've especially enjoyed solving difficult and technical problems, which has inspired me to seek out software development roles.",
    fullWidth: true,
  },
  {
    text: "For the past 4 years I've conducted brain research on NASA astronauts and in terrestrial spaceflight analogues. This has led to my authorship on 4 papers and presentation at NASA's Human Research Program Investigator's Workshop. <p> Much of my work has been investigating structural changes in the brain due to weightlessness, such as the upward brain shift and crowding at the vertex of the skull that you see on the left. </p>",
    img: "/biopics/braingif.gif",
  },
  {
    text: "Through my research I've developed skills and software competencies; the most important of these are descriptive and inferential statistical analysis, as well as image analytic techniques, such as image registration, segmentation, filtering, and mathematical modeling. <p> I use Python's Pandas and statsmodels for statistical modeling (see <a href='https://github.com/andrew-taylor-2/Time-Series-Regressions-in-Pandas/blob/main/Time%20Series%20Analysis.ipynb' style='color: #add8e6;'>this repo</a> for an example of how I extracted trends from the astronauts' pre- to postflight cognitive measure changes). For image analysis, I use MATLAB and Python with numpy and the OpenCV library.</p> ",
    img: "/biopics/pic2.png",
  },
  {
    text: "I've combined my Python skills with my love for the ancient board game Go to create a computer vision app. On the 'Board' tab of this website, you'll find a Go board. Upload an image of a game, and the app will use OpenCV tools to identify the positions and render the board, allowing you to continue playing here on the website.",
    fullWidth: true,
  },
  {}, // this is to fix the modulo 2 so that the pics still zig zag
  {
    text: "Building this website has provided some opportunities for learning new skills as well. I'm using a React.js frontend that communicates with my Python backend image processing app via FastAPI. The application is hosted on an AWS EC2 instance with Nginx as the web server. User submissions are stored in a PostgreSQL database. I've also learned about networking, efficiently using cloud computing resources, and security considerations.",
    img: "/biopics/pic3.png",
  },
];

const Bio = () => {
    return (
      <>
        {globalStyles}
        <Container maxWidth="lg" sx={{ padding: '0rem 0' }}>
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
                    width: index === 0 ? '35%' : '50%', // Adjust the size of the first image
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
                  padding: '0rem',
                  textAlign: item.fullWidth ? 'center' : 'left',
                }}
                dangerouslySetInnerHTML={{ __html: item.text }}
              />
            </Box>
          ))}
        </Container>
      </>
    );
  };

export default Bio;


