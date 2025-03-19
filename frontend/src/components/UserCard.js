import { Avatar, Box, Card, CardBody, CardHeader, Flex, Heading, IconButton, Text, useToast } from "@chakra-ui/react";
import { BiTrash } from "react-icons/bi";
import EditModal from "./EditModal";
import { BASE_URL } from "../App";

const UserCard = ({ user, setUsers }) => {
  const toast = useToast();
  const handleDeleteUser = async () => {
    try {
      const response = await fetch(BASE_URL + "/friends/delete/" + user.id, {
        method: "PATCH",
      });
      if (!response.ok) {
        throw new Error("Failed to delete user");
      }
      setUsers((prevUsers) => prevUsers.filter((u) => u.id !== user.id));
      toast({
        title: "User deleted",
        status: "success",
        duration: 2000,
        isClosable: true,
        position: "top-center",
      });
    } catch (error) {
      console.error(error);
      toast({
        title: "Failed to delete user",
        status: "error",
        duration: 4000,
        isClosable: true,
        position: "top-center",
      });
    }
  }
  return (
      <Card>
        <CardHeader>
          <Flex gap={4}>
            <Flex flex={"1"} gap={"4"} alignItems={"center"}>
              <Avatar src={user.img_url}/>
  
              <Box>
                <Heading size='sm'>{user.name}</Heading>
                <Text>{user.role}</Text>
              </Box>
            </Flex>
  
            <Flex>
              <EditModal user={user} setUsers={setUsers}/>
              <IconButton
                variant='ghost'
                colorScheme='red'
                size={"sm"}
                aria-label='See menu'
                icon={<BiTrash size={20} />}
                onClick={handleDeleteUser}
              />
            </Flex>
          </Flex>
        </CardHeader>
  
        <CardBody>
          <Text>{user.description}</Text>
        </CardBody>
      </Card>
  )
}

export default UserCard;
