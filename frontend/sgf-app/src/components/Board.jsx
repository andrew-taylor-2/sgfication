import React, { useEffect, useState } from 'react';
import { Goban } from '@sabaki/shudan';
import '@sabaki/shudan/css/goban.css';
import sgf from '@sabaki/sgf';
import GoBoard from "@sabaki/go-board";
import axios from 'axios';
import { Box, useTheme, useMediaQuery } from '@mui/material';

const defaultBoardSize = 19;
const defaultSignMap = Array.from({ length: defaultBoardSize }, () => Array(defaultBoardSize).fill(0));

const Board = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [signMap, setSignMap] = useState(defaultSignMap);
  const [vertexSize, setVertexSize] = useState(isMobile ? 12 : 24);
  const [showCoordinates, setShowCoordinates] = useState(false);
  const [showCorner, setShowCorner] = useState(false);
  const [fuzzyStonePlacement, setFuzzyStonePlacement] = useState(true);
  const [animateStonePlacement, setAnimateStonePlacement] = useState(true);
  const [isBusy, setIsBusy] = useState(false);
  const [file, setFile] = useState(null);
  const [sgfData, setSgfData] = useState(null);
  const [isBlackTurn, setIsBlackTurn] = useState(true);

  useEffect(() => {
    if (sgfData) {
      const parseSGF = (sgfData) => {
        const collection = sgf.parse(sgfData);
        const gameTree = collection[0];
        const rootNode = gameTree.data;
        const boardSize = parseInt(rootNode.SZ[0]);
        const signMap = Array.from({ length: boardSize }, () => Array(boardSize).fill(0));

        const parseCoordinates = (coords) => {
          return coords.map(coord => {
            const x = coord.charCodeAt(0) - 97;
            const y = coord.charCodeAt(1) - 97;
            return [x, y];
          });
        };

        if (rootNode.AB) {
          parseCoordinates(rootNode.AB).forEach(([x, y]) => {
            signMap[y][x] = 1;
          });
        }

        if (rootNode.AW) {
          parseCoordinates(rootNode.AW).forEach(([x, y]) => {
            signMap[y][x] = -1;
          });
        }

        return signMap;
      };

      const newSignMap = parseSGF(sgfData);
      setSignMap(newSignMap);
    }
  }, [sgfData]);

  useEffect(() => {
    setVertexSize(isMobile ? 12 : 24);
  }, [isMobile]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const apiUrl = import.meta.env.VITE_API_URL;
      const response = await axios.post(`${apiUrl}/analyze/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setSgfData(response.data.sgf);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleStonePlace = (evt, [x, y]) => {
    // Only handle left clicks (button === 0)
    if (evt.button === 0) {
      const sign = isBlackTurn ? 1 : -1; // 1 for black, -1 for white
      const newBoard = new GoBoard(signMap);
      const nBm = newBoard.makeMove(sign, [x, y]);
      setSignMap(nBm.signMap);
      setIsBlackTurn(!isBlackTurn); // Toggle turn
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: { xs: 'column', sm: 'row' },
        gap: 2,
        width: '100%',
        alignItems: { xs: 'center', sm: 'flex-start' },
        justifyContent: 'center',
        maxWidth: '100vw',
        overflow: 'hidden'
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 1,
          width: { xs: '100%', sm: 'auto' }
        }}
      >
        <form style={{ display: 'flex', flexDirection: 'column' }}>
          <p style={{ margin: '0 0 .5em 0' }}>
            Size:
            <button type="button" onClick={() => setVertexSize(Math.max(vertexSize - 4, 4))}>-</button>
            <button type="button" title="Reset" onClick={() => setVertexSize(isMobile ? 12 : 24)}>•</button>
            <button type="button" onClick={() => setVertexSize(vertexSize + 4)}>+</button>
          </p>
          <p style={{ margin: '0 0 .5em 0' }}>
            Stones:
            <button type="button" title="Reset" onClick={() => {
              setSignMap(defaultSignMap);
              setIsBlackTurn(true); // Reset turn to black when clearing board
            }}>•</button>
          </p>
          <label>
            <input 
              type="checkbox" 
              checked={showCoordinates} 
              onChange={() => setShowCoordinates(!showCoordinates)} 
            />
            Show coordinates
          </label>
          <label>
            <input 
              type="checkbox" 
              checked={isBusy} 
              onChange={() => setIsBusy(!isBusy)} 
            />
            Busy
          </label>
        </form>
      </Box>

      <Box
        sx={{
          maxWidth: '100%',
          overflow: 'visible',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center'
        }}
      >
        <div onContextMenu={(evt) => evt.preventDefault()}>
          <Goban
            vertexSize={vertexSize}
            animate={true}
            busy={isBusy}
            rangeX={showCorner ? [8, 18] : undefined}
            rangeY={showCorner ? [12, 18] : undefined}
            signMap={signMap}
            showCoordinates={showCoordinates}
            fuzzyStonePlacement={fuzzyStonePlacement}
            animateStonePlacement={animateStonePlacement}
            onVertexMouseUp={handleStonePlace}
          />
        </div>

        <Box sx={{ mt: 2, width: '100%', textAlign: 'center' }}>
          <h2>Upload a picture of a Go board to continue play here!</h2>
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleFileUpload}>Upload</button>
        </Box>
      </Box>
    </Box>
  );
};

export default Board;