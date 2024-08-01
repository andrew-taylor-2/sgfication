import React, { useEffect, useState } from 'react';
import { Goban } from '@sabaki/shudan';
import '@sabaki/shudan/css/goban.css';
import sgf from '@sabaki/sgf'; // Import the SGF parser

const Board = ({ sgfData }) => {
  const [signMap, setSignMap] = useState([]);
  useEffect(() => {
    const parseSGF = (sgfData) => {
      const collection = sgf.parse(sgfData);
      const gameTree = collection[0];
      const rootNode = gameTree.data;
      const boardSize = parseInt(rootNode.SZ[0]);
      const signMap = Array.from({ length: boardSize }, () => Array(boardSize).fill(0)); // Initialize a 2D array with 0 (empty)

      const parseCoordinates = (coords) => {
        return coords.map(coord => {
          const x = coord.charCodeAt(0) - 97;
          const y = coord.charCodeAt(1) - 97;
          return [x, y];
        });
      };

      if (rootNode.AB) {
        parseCoordinates(rootNode.AB).forEach(([x, y]) => {
          signMap[y][x] = 1; // Black stones
        });
      }

      if (rootNode.AW) {
        parseCoordinates(rootNode.AW).forEach(([x, y]) => {
          signMap[y][x] = -1; // White stones
        });
      }

      return signMap;
    };

    const newSignMap = parseSGF(sgfData);
    setSignMap(newSignMap);
  }, [sgfData]);

  return (
    <div>
      <div>
        <Goban vertexSize={24} signMap={signMap} />
      </div>
    </div>
  );
};

export default Board;
