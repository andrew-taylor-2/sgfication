import React, { useEffect, useState } from 'react';
import { Goban } from '@sabaki/shudan';
import '@sabaki/shudan/css/goban.css';
import sgf from '@sabaki/sgf'; // Import the SGF parser

const Board = ({ sgfData }) => {
  const [signMap, setSignMap] = useState([]);

  useEffect(() => {
    const parseSGF = (sgfData) => {
      const collection = sgf.parse(sgfData);
      const gameTree = collection.gameTrees[0];
      const rootNode = gameTree.nodes[0];
      const boardSize = rootNode.SZ[0];
      const signMap = Array.from({ length: boardSize }, () => Array(boardSize).fill(0)); // Initialize a 2D array with 0 (empty)

      gameTree.nodes.forEach((node) => {
        if (node.B) {
          const [x, y] = node.B[0];
          signMap[x][y] = 1; // Black stone
        } else if (node.W) {
          const [x, y] = node.W[0];
          signMap[x][y] = -1; // White stone
        }
      });

      return signMap;
    };

    if (sgfData) {
      setSignMap(parseSGF(sgfData));
    }
  }, [sgfData]);

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ width: '500px', height: '500px' }}> {/* Set the desired size */}
        <Goban vertexSize={24} signMap={signMap} />
      </div>
    </div>
  );
};

export default Board;
