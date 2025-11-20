import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { Toaster } from "@/components/ui/toaster";
import { LogIn, UserPlus } from "lucide-react";
import { loginUser, registerUser } from "@/services/authService";

export default function AuthPage() {
  const { toast } = useToast();

  const [loginData, setLoginData] = useState({ email: "", password: "" });
  const [registerData, setRegisterData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleLogin = async () => {
    try {
      await loginUser(loginData.email, loginData.password);
      toast({ title: "Login bem-sucedido 🎉", description: "Bem-vindo de volta!" });
      window.location.href = "/home"; 
    } catch (error: any) {
      toast({
        title: "Erro no login",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const handleRegister = async () => {
    try {
      await registerUser(registerData.name, registerData.email, registerData.password);
      toast({
        title: "Conta criada 🥳",
        description: "Você já pode fazer login agora!",
      });
    } catch (error: any) {
      toast({
        title: "Erro no registro",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-6">
      <div className="max-w-5xl w-full grid md:grid-cols-2 gap-8">
        {/* LOGIN */}
        <Card className="shadow-xl border-2">
          <CardHeader className="text-center">
            <CardTitle className="flex items-center justify-center gap-2 text-2xl text-primary">
              <LogIn className="w-6 h-6" /> Login
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="Email"
              type="email"
              value={loginData.email}
              onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
            />
            <Input
              placeholder="Senha"
              type="password"
              value={loginData.password}
              onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
            />
            <Button className="w-full" onClick={handleLogin}>
              Entrar
            </Button>
          </CardContent>
        </Card>

        {/* REGISTRO */}
        <Card className="shadow-xl border-2">
          <CardHeader className="text-center">
            <CardTitle className="flex items-center justify-center gap-2 text-2xl text-primary">
              <UserPlus className="w-6 h-6" /> Criar Conta
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              placeholder="Nome"
              value={registerData.name}
              onChange={(e) =>
                setRegisterData({ ...registerData, name: e.target.value })
              }
            />
            <Input
              placeholder="Email"
              type="email"
              value={registerData.email}
              onChange={(e) =>
                setRegisterData({ ...registerData, email: e.target.value })
              }
            />
            <Input
              placeholder="Senha"
              type="password"
              value={registerData.password}
              onChange={(e) =>
                setRegisterData({ ...registerData, password: e.target.value })
              }
            />
            <Button className="w-full" onClick={handleRegister}>
              Registrar
            </Button>
          </CardContent>
        </Card>
      </div>
      <Toaster />
    </div>
  );
}
