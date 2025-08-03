import React from "react";
import { motion } from "framer-motion";

export const SplitText = ({ text, delay = 50 }) => {
  return (
    <div style={{ display: "inline-block" }}>
      {Array.from(text).map((char, index) => (
        <motion.span
          key={index}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * (delay / 1000), duration: 0.05 }}
          style={{ display: "inline-block" }}
        >
          {char === " " ? "\u00A0" : char} {/* Preserve spaces */}
        </motion.span>
      ))}
    </div>
  );
};
