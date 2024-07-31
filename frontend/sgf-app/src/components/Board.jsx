import React, { useEffect, useState } from 'react';
import { Goban } from '@sabaki/shudan';
import '@sabaki/shudan/css/goban.css';
import sgf from '@sabaki/sgf'; // Import the SGF parser

const Board = ({ sgfData }) => {
  const [signMap, setSignMap] = useState({});

  useEffect(() => {
    const parseSGF = (sgfData) => {
      const collection = sgf.parse(sgfData);
      const gameTree = collection.gameTrees[0];
      const rootNode = gameTree.nodes[0];
      const boardSize = rootNode.SZ[0];
      const signMap = {};

      // Initialize an empty sign map
      for (let x = 0; x < boardSize; x++) {
        for (let y = 0; y < boardSize; y++) {
          const vertex = `${String.fromCharCode(97 + x)}${String.fromCharCode(97 + y)}`;
          signMap[vertex] = null;
        }
      }

      // Process nodes to populate the sign map
      gameTree.nodes.forEach((node) => {
        if (node.B) {
          const [x, y] = node.B[0];
          const vertex = `${String.fromCharCode(97 + x)}${String.fromCharCode(97 + y)}`;
          signMap[vertex] = 'B';
        } else if (node.W) {
          const [x, y] = node.W[0];
          const vertex = `${String.fromCharCode(97 + x)}${String.fromCharCode(97 + y)}`;
          signMap[vertex] = 'W';
        }
      });

      return signMap;
    };

    if (sgfData) {
      setSignMap(parseSGF(sgfData));
    }
  }, [sgfData]);

  return (
    <div>
      <Goban vertexSize={24} signMap={signMap} />
    </div>
  );
};

export default Board;
