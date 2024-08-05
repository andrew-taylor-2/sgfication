import React, { useEffect, useState } from 'react';
import { Goban } from '@sabaki/shudan';
import '@sabaki/shudan/css/goban.css';
import sgf from '@sabaki/sgf'; // SGF parser
import GoBoard from "@sabaki/go-board" // board class

const defaultBoardSize = 19;
const defaultSignMap = Array.from({ length: defaultBoardSize }, () => Array(defaultBoardSize).fill(0));

const Board = ({ sgfData }) => {
  const [signMap, setSignMap] = useState(defaultSignMap);
  const [vertexSize, setVertexSize] = useState(24);
  const [showCoordinates, setShowCoordinates] = useState(false);
  const [alternateCoordinates, setAlternateCoordinates] = useState(false);
  const [showCorner, setShowCorner] = useState(false);
  const [fuzzyStonePlacement, setFuzzyStonePlacement] = useState(false);
  const [animateStonePlacement, setAnimateStonePlacement] = useState(false);
  const [isBusy, setIsBusy] = useState(false);

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
    }
  }, [sgfData]);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '15em auto', gridColumnGap: '1em' }}>
      <form style={{ display: 'flex', flexDirection: 'column' }}>
        <p style={{ margin: '0 0 .5em 0' }}>
          Size: 
          <button type="button" onClick={() => setVertexSize(Math.max(vertexSize - 4, 4))}>-</button>
          <button type="button" title="Reset" onClick={() => setVertexSize(24)}>•</button>
          <button type="button" onClick={() => setVertexSize(vertexSize + 4)}>+</button>
        </p>
        <p style={{ margin: '0 0 .5em 0' }}>
          Stones: 
          <button type="button" title="Reset" onClick={() => setSignMap(defaultSignMap)}>•</button>
        </p>
        <label>
          <input type="checkbox" checked={showCoordinates} onChange={() => setShowCoordinates(!showCoordinates)} />
          Show coordinates
        </label>
        <label>
          <input type="checkbox" checked={alternateCoordinates} onChange={() => setAlternateCoordinates(!alternateCoordinates)} />
          Alternate coordinates
        </label>
        <label>
          <input type="checkbox" checked={isBusy} onChange={() => setIsBusy(!isBusy)} />
          Busy
        </label>
        {/* Add other checkboxes as needed */}
      </form>

      <div>
        <Goban
          vertexSize={vertexSize}
          animate={true}
          busy={isBusy}
          rangeX={showCorner ? [8, 18] : undefined}
          rangeY={showCorner ? [12, 18] : undefined}
          coordX={alternateCoordinates ? (i) => chineseCoord[i] : undefined}
          coordY={alternateCoordinates ? (i) => i + 1 : undefined}
          signMap={signMap}
          showCoordinates={showCoordinates}
          fuzzyStonePlacement={fuzzyStonePlacement}
          animateStonePlacement={animateStonePlacement}
          // Add other Goban props as needed
          onVertexMouseUp={(evt, [x, y]) => {
            const sign = evt.button === 0 ? 1 : -1;
            const newBoard = new GoBoard(signMap);
            const nBm = newBoard.makeMove(sign, [x, y]);
            setSignMap(nBm.signMap);
          }}
        />
        {alternateCoordinates && (
          <style>{`
            .shudan-coordx span {
              font-size: .45em;
            }
          `}</style>
        )}
      </div>
    </div>
  );
};

export default Board;
